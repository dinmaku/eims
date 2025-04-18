#routes.py
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import (
    check_user, create_user, get_user_wishlist, 
    get_user_id_by_email, create_outfit, get_outfits, get_outfit_by_id, 
    book_outfit, get_booked_wishlist_by_user, delete_booked_wishlist, 
    get_package_details_by_id, get_booked_outfits_by_user,  
    get_available_suppliers, get_available_venues, get_available_gown_packages, 
    get_event_types, get_all_additional_services, get_booked_schedules, add_event_item,
    create_wishlist_package, initialize_test_suppliers, get_user_profile_by_id,
    change_password, get_db_connection, update_user_profile_picture, get_client_packages
)
import logging
import jwt
from functools import wraps
import os
from datetime import datetime, date, time
from werkzeug.utils import secure_filename
import uuid

logging.basicConfig(level=logging.DEBUG)

def init_routes(app):
    
    @app.route('/login', methods=['POST'])
    def login():
        try:
            # Get the login data
            data = request.json
            identifier = data.get('identifier')  # Can be email or username
            password = data.get('password')

            # Check if identifier and password are provided
            if not identifier or not password:
                return jsonify({'message': 'Username/Email and password are required!'}), 400

            # Check the user credentials
            is_valid, user_type = check_user(identifier, password)
            if is_valid:
                # Generate JWT token with additional claims
                access_token = create_access_token(identity=identifier, additional_claims={"user_type": user_type})

                return jsonify({
                    'message': 'Login successful!',
                    'access_token': access_token,
                    'user_type': user_type
                }), 200
            else:
                return jsonify({'message': 'Invalid username/email or password.'}), 401

        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({'message': 'An error occurred during login.'}), 500

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        print(data)  # Log the incoming data for debugging
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        username = data.get('username')
        email = data.get('email')
        contact_number = data.get('contactNumber')
        password = data.get('password')
        address = data.get('address', '') 
        user_type = 'Client'  # Default user type

        # Validate required fields
        if not all([first_name, last_name, username, email, contact_number, password]):
            return jsonify({'message': 'All fields are required!'}), 400

        # Attempt to create the user
        if create_user(first_name, last_name, username, email, contact_number, password, user_type, address):
            return jsonify({'message': 'Registration successful!'}), 201
        else:
            return jsonify({'message': 'Email already exists!'}), 409

    @app.route('/available-suppliers', methods=['GET'])
    @jwt_required()
    def get_available_suppliers_route():
        try:
            suppliers = get_available_suppliers()
            return jsonify(suppliers), 200
        except Exception as e:
            app.logger.error(f"Error fetching available suppliers: {e}")
            return jsonify({'message': 'An error occurred while fetching available suppliers'}), 500

    @app.route('/available-venues', methods=['GET'])
    @jwt_required()
    def get_available_venues_route():
        try:
            venues = get_available_venues()
            return jsonify(venues), 200
        except Exception as e:
            app.logger.error(f"Error fetching available venues: {e}")
            return jsonify({'message': 'An error occurred while fetching available venues'}), 500

    @app.route('/available-gown-packages', methods=['GET'])
    @jwt_required()
    def get_available_gown_packages_route():
        try:
            gown_packages = get_available_gown_packages()
            return jsonify(gown_packages), 200
        except Exception as e:
            app.logger.error(f"Error fetching available gown packages: {e}")
            return jsonify({'message': 'An error occurred while fetching available gown packages'}), 500

    @app.route('/packages/<int:package_id>', methods=['GET'])
    @jwt_required()
    def get_package_details(package_id):
        try:
            package = get_package_details_by_id(package_id)  # Implement this function to fetch package details
            if not package:
                return jsonify({'message': 'Package not found'}), 404
            return jsonify(package), 200
        except Exception as e:
            app.logger.error(f"Error fetching package details: {e}")
            return jsonify({'message': 'An error occurred while fetching package details'}), 500

    @app.route('/wishlist', methods=['GET'])
    @jwt_required()
    def get_wishlist():
        email = get_jwt_identity()
        userid = get_user_id_by_email(email)
        print(f"User ID from email: {userid}")  # Debug statement
        wishlist = get_user_wishlist(userid)

        return jsonify(wishlist), 200

    SECRET_KEY = os.getenv('eims', 'fallback_jwt_secret')

# Decorator to protect routes and check token
    def token_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'msg': 'Token is missing'}), 403

            try:
                # Remove 'Bearer ' from the token string
                token = token.split(" ")[1]
                # Decode the token using the secret key
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify({'msg': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'msg': 'Invalid token'}), 401

            # Token is valid, pass control to the original route function
            return f(decoded_token, *args, **kwargs)

        return decorated_function
    
    @app.route('/check-auth', methods=['GET'])
    @jwt_required()
    def check_auth():
        try:
            # Access the identity from the decoded JWT token
            current_user = get_jwt_identity()  # This is the email (identity) you set in the JWT token
            return jsonify({"msg": f"Token is valid for user: {current_user}"}), 200
        except Exception as e:
            return jsonify({'msg': f'Error: {str(e)}'}), 422
        
    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token)

    @app.route('/logout', methods=['POST'])
    def logout():
       
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/outfits', methods=['POST'])
    @jwt_required()
    def add_outfit():
        try:
            data = request.json
            outfit_name = data.get('outfit_name')
            outfit_type = data.get('outfit_type')
            outfit_color = data.get('outfit_color')
            outfit_desc = data.get('outfit_desc')
            rent_price = data.get('rent_price')
            status = data.get('status')
            outfit_img = data.get('outfit_img')

            # Validate required fields
            if not all([outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img]):
                return jsonify({'message': 'All fields are required!'}), 400

            # Create the new outfit
            if create_outfit(outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img):
                return jsonify({'message': 'Outfit added successfully!'}), 201
            else:
                return jsonify({'message': 'Error adding outfit'}), 500
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500

    @app.route('/outfits', methods=['GET'])
    def get_all_outfits():
        try:
            outfits = get_outfits()
            return jsonify(outfits), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching outfits: {str(e)}'}), 500

    @app.route('/outfits/<int:outfit_id>', methods=['GET'])
    @jwt_required()
    def get_outfit(outfit_id):
        try:
            outfit = get_outfit_by_id(outfit_id)
            if outfit:
                return jsonify(outfit), 200
            else:
                return jsonify({'message': 'Outfit not found'}), 404
        except Exception as e:
            return jsonify({'message': f'Error fetching outfit: {str(e)}'}), 500

    @app.route('/book-outfit', methods=['POST'])
    @jwt_required()
    def book_outfit_route():
        try:
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)  # Assuming this function exists

            data = request.json
            outfit_id = data.get('outfit_id')
            pickup_date = data.get('pickup_date')
            return_date = data.get('return_date')
            status = data.get('status')
            additional_charges = data.get('additional_charges', 0)

            if book_outfit(userid, outfit_id, pickup_date, return_date, status, additional_charges):
                return jsonify({'message': 'Outfit booked successfully!'}), 201
            else:
                return jsonify({'message': 'Error booking outfit'}), 500
        except Exception as e:
            return jsonify({'message': f'Error booking outfit: {str(e)}'}), 500

    @app.route('/booked-wishlist', methods=['GET'])
    @jwt_required()
    def get_user_booked_wishlist():
        try:
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)  # Assuming a function to get user ID by email exists

            # Fetch events for the user from the updated events table
            booked_wishlist = get_booked_wishlist_by_user(userid)
            return jsonify(booked_wishlist), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching booked wishlist: {str(e)}'}), 500

    @app.route('/booked_wishlist/<int:events_id>', methods=['DELETE'])
    @jwt_required()  # Assuming you're using JWT for authorization
    def delete_wishlist_item(events_id):
        try:
            # Call the function to delete the event item by events_id
            if delete_booked_wishlist(events_id):
                return jsonify({"message": "Event item deleted successfully"}), 200
            else:
                return jsonify({"message": "Failed to delete event item"}), 500
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500

    @app.route('/booked-outfits', methods=['GET'])
    @jwt_required()
    def get_user_booked_outfits():
        try:
            # Fetch the current user's email from the JWT token
            email = get_jwt_identity()
            
            # Here, you would fetch the user's ID based on their email (you can create a helper function for this)
            # Assuming you have a function to get the user ID from email
            userid = get_user_id_by_email(email)
            
            # Fetch the booked outfits for the user
            booked_outfits = get_booked_outfits_by_user(userid)
            
            # Return the fetched data as JSON
            return jsonify(booked_outfits), 200
        except Exception as e:
            # If there's an error, return a message with the error details
            return jsonify({'message': f'Error fetching booked outfits: {str(e)}'}), 500

    #packages routes
    @app.route('/created-packages', methods=['GET', 'OPTIONS'])
    def get_packages_route():
        """
        Route for fetching all event packages.
        OPTIONS: Handles CORS preflight requests
        GET: Returns a list of all event packages
        """
        # Handle OPTIONS requests for CORS preflight
        if request.method == 'OPTIONS':
            return jsonify({'message': 'OK'}), 200
            
        try:
            # Get packages formatted for client use
            packages = get_client_packages()
            
            # Format the results
            formatted_packages = []
            for package in packages:
                # Process venue image path if venue exists
                venue_image = None
                if package.get('venue_id'):
                    venue_image = package.get('venue_image')
                    if venue_image:
                        # Handle different path formats
                        if '\\' in venue_image:
                            venue_image = venue_image.split('\\')[-1]
                        elif '/' in venue_image:
                            venue_image = venue_image.split('/')[-1]
                        
                        # If the image is one of our static images, use direct static path
                        static_images = ['grandballroom.png', 'hogwarts.png', 'oceanview.png', 'paseo.png', 'sealavie.png']
                        if any(venue_image.endswith(img) for img in static_images):
                            venue_image = f'/img/venues-img/{venue_image}'
                        # For uploaded images, use API endpoint
                        else:
                            venue_image = f'/api/venue-image/{venue_image}'
                
                formatted_packages.append({
                    'package_id': package['package_id'],
                    'package_name': package['package_name'],
                    'capacity': package['capacity'],
                    'description': package['description'],
                    'additional_capacity_charges': float(package['additional_capacity_charges']) if package['additional_capacity_charges'] else 0,
                    'charge_unit': package['charge_unit'],
                    'total_price': float(package['total_price']) if package['total_price'] else 0,
                    'status': package['status'],
                    'venue': {
                        'name': package['venue_name'],
                        'location': package.get('location'),
                        'price': float(package.get('venue_price', 0)),
                        'capacity': package.get('venue_capacity'),
                        'description': package.get('venue_description'),
                        'image': venue_image
                    } if package.get('venue_name') else None,
                    'event_type': package.get('event_type_name'),
                    'gown_package': {
                        'name': package.get('gown_package_name'),
                        'price': float(package.get('gown_package_price', 0)),
                        'description': package.get('gown_package_description')
                    } if package.get('gown_package_name') else None,
                    'suppliers': package.get('suppliers', []),
                    'additional_services': package.get('additional_services', [])
                })
            
            return jsonify(formatted_packages), 200
        except Exception as e:
            # Log any errors that occur
            app.logger.error(f"Error fetching packages: {str(e)}")
            
            # Return a 500 error with details
            return jsonify({
                'message': 'An error occurred while fetching packages',
                'error': str(e)
            }), 500

    @app.route('/event-types', methods=['GET'])
    def get_event_types_route():
        try:
            event_types = get_event_types()
            return jsonify(event_types), 200
        except Exception as e:
            app.logger.error(f"Error fetching event types: {e}")
            return jsonify({"error": str(e)}), 500

    #additional services routes
    @app.route('/created-services', methods=['GET'])
    @jwt_required()
    def get_services_route():
        try:
            services = get_all_additional_services()
            return jsonify(services), 200
        except Exception as e:
            app.logger.error(f"Error fetching services: {e}")
            return jsonify({'message': 'An error occurred while fetching services'}), 500

    @app.route('/api/events/schedules', methods=['GET'])
    @jwt_required()
    def get_booked_schedules_route():
        try:
            schedules = get_booked_schedules()
            return jsonify(schedules)
        except Exception as e:
            app.logger.error(f"Error in get_booked_schedules route: {str(e)}")
            return jsonify({'error': str(e)}), 422

    @app.route('/events', methods=['POST', 'OPTIONS'])
    @jwt_required()
    def create_event():
        if request.method == 'OPTIONS':
            # Handle preflight request
            response = jsonify({'message': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
            
        try:
            # Get user ID from JWT token
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)
            
            if not userid:
                response = jsonify({
                    'success': False,
                    'message': 'Invalid user token'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 401

            data = request.get_json()
            
            # Extract base event data
            event_data = {
                'userid': userid,  # Use the userid from JWT token
                'event_name': data.get('event_name'),
                'event_type': data.get('event_type'),
                'event_theme': data.get('event_theme'),
                'event_color': data.get('event_color'),
                'package_id': data.get('package_id'),
                'schedule': data.get('schedule'),
                'start_time': data.get('start_time'),
                'end_time': data.get('end_time'),
                'status': data.get('status', 'Wishlist'),
                'total_price': data.get('total_price', 0),
                'booking_type': data.get('booking_type', 'Online')  # Add booking_type with default value 'Online'
            }

            # Package configuration data
            package_config = {
                'suppliers': data.get('suppliers', []),
                'outfits': data.get('outfits', []),
                'services': data.get('services', []),
                'additional_items': data.get('additional_items', [])
            }

            # Process additional services to ensure correct format
            if 'additional_services' in data:
                for service in data['additional_services']:
                    # Map service_id to add_service_id if needed
                    if 'service_id' in service and 'add_service_id' not in service:
                        service['add_service_id'] = service['service_id']

            # If services come from inclusions array, extract them
            if 'inclusions' in data and not data.get('services'):
                data['services'] = []
                for inclusion in data['inclusions']:
                    if inclusion['type'] == 'service' and 'data' in inclusion:
                        service_data = inclusion['data']
                        # Ensure it has service_id
                        if 'service_id' in service_data or 'add_service_id' in service_data:
                            data['services'].append(service_data)
            
            # If suppliers come from inclusions array, extract them
            if 'inclusions' in data and not data.get('suppliers'):
                data['suppliers'] = []
                for inclusion in data['inclusions']:
                    if inclusion['type'] == 'supplier' and 'data' in inclusion:
                        supplier_data = inclusion['data']
                        # Ensure it has supplier_id
                        if 'supplier_id' in supplier_data:
                            data['suppliers'].append(supplier_data)
            
            # If outfits come from inclusions array, extract them
            if 'inclusions' in data and not data.get('outfits'):
                data['outfits'] = []
                for inclusion in data['inclusions']:
                    if inclusion['type'] == 'outfit' and 'data' in inclusion:
                        outfit_data = inclusion['data']
                        # Handle gown_package_id which might be called outfit_id in the frontend
                        if 'outfit_id' in outfit_data and not outfit_data.get('gown_package_id'):
                            outfit_data['gown_package_id'] = outfit_data['outfit_id']
                        data['outfits'].append(outfit_data)

            # Ensure consistent field names for services array
            if 'services' not in data and 'additional_services' in data:
                data['services'] = data['additional_services']

            # Add event and its configurations
            events_id = add_event_item(**event_data, **package_config)

            if events_id:
                response = jsonify({
                    'success': True,
                    'message': 'Event created successfully',
                    'events_id': events_id
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 201
            else:
                response = jsonify({
                    'success': False,
                    'message': 'Failed to create event'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 500

        except Exception as e:
            app.logger.error(f"Error creating event: {str(e)}")
            response = jsonify({
                'success': False,
                'message': f'Error creating event: {str(e)}'
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/wishlist-packages', methods=['POST', 'OPTIONS'])
    @jwt_required()
    def create_wishlist_package_route():
        if request.method == 'OPTIONS':
            # Handle preflight request
            response = jsonify({'message': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
            
        try:
            # Get user ID from token
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)
            
            if userid is None:
                response = jsonify({
                    'success': False,
                    'message': 'User not found'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 404

            data = request.get_json()
            app.logger.info(f"Received wishlist package data: {data}")

            # Process venue data for the wishlist_venues table
            if 'inclusions' in data:
                # Extract venue data from inclusions if available
                venue_inclusion = next((item for item in data['inclusions'] if item['type'] == 'venue'), None)
                if venue_inclusion and 'data' in venue_inclusion:
                    venue_data = venue_inclusion['data']
                    data['venue'] = venue_data
                    
                    # Ensure venue_id is set at the top level
                    if 'venue_id' in venue_data and not data.get('venue_id'):
                        data['venue_id'] = venue_data['venue_id']
                    
                    # Make sure the venue price is extracted correctly
                    if 'venue_price' in venue_data:
                        # Log the venue price from the inclusion
                        app.logger.info(f"Found venue price in inclusions: {venue_data['venue_price']}")
                    else:
                        # If venue_price isn't in the data, try to get it from the database
                        try:
                            venue_id = venue_data['venue_id']
                            cursor = get_db_connection().cursor()
                            cursor.execute("SELECT venue_price FROM venues WHERE venue_id = %s", (venue_id,))
                            result = cursor.fetchone()
                            if result and result[0]:
                                venue_data['venue_price'] = float(result[0])
                                app.logger.info(f"Retrieved venue price from database: {venue_data['venue_price']}")
                            cursor.close()
                        except Exception as e:
                            app.logger.error(f"Error fetching venue price: {e}")
            
            # Log the final venue data for debugging
            if 'venue' in data:
                app.logger.info(f"Final venue data being passed to create_wishlist_package: {data['venue']}")

            # Check if outfit is in inclusions, if not, set gown_package_id to NULL
            outfit_inclusion = next((item for item in data['inclusions'] if item['type'] == 'outfit'), None)
            if not outfit_inclusion:
                # If no outfit inclusion exists, set gown_package_id to None
                data['gown_package_id'] = None
            elif 'data' in outfit_inclusion:
                # Set gown_package_id from outfit data
                if 'outfit_id' in outfit_inclusion['data'] and not outfit_inclusion['data'].get('gown_package_id'):
                    data['gown_package_id'] = outfit_inclusion['data']['outfit_id']
                elif 'gown_package_id' in outfit_inclusion['data']:
                    data['gown_package_id'] = outfit_inclusion['data']['gown_package_id']

            # Log the final data going into create_wishlist_package
            app.logger.info(f"Final data being sent to create_wishlist_package:")
            app.logger.info(f"- events_id: {data.get('events_id')}")
            app.logger.info(f"- venue_id: {data.get('venue_id')}")
            app.logger.info(f"- gown_package_id: {data.get('gown_package_id')}")
            
            if 'inclusions' in data:
                service_inclusions = [inc for inc in data['inclusions'] if inc['type'] == 'service']
                app.logger.info(f"- service inclusions count: {len(service_inclusions)}")
                for i, inc in enumerate(service_inclusions):
                    app.logger.info(f"  - Service {i+1}: {inc.get('data', {}).get('service_id') or inc.get('data', {}).get('add_service_id')}")

            # Create wishlist package and its related data
            wishlist_id = create_wishlist_package(
                events_id=data.get('events_id'),
                package_data=data
            )

            if wishlist_id:
                response = jsonify({
                    'success': True,
                    'message': 'Wishlist package created successfully',
                    'wishlist_id': wishlist_id
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 201
            else:
                response = jsonify({
                    'success': False,
                    'message': 'Failed to create wishlist package'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 500

        except Exception as e:
            app.logger.error(f"Error creating wishlist package: {str(e)}")
            response = jsonify({
                'success': False,
                'message': f'Error creating wishlist package: {str(e)}'
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/api/suppliers', methods=['GET'])
    def get_suppliers():
        try:
            suppliers = get_available_suppliers()
            
            # For debugging purposes
            logging.info(f"Suppliers data: {suppliers}")
            
            response = jsonify({
                'status': 'success',
                'data': suppliers
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
        except Exception as e:
            logging.error(f"Error fetching suppliers: {e}")
            response = jsonify({
                'status': 'error',
                'message': str(e)
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/api/init-test-suppliers', methods=['POST'])
    def init_test_suppliers():
        try:
            success = initialize_test_suppliers()
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Test suppliers initialized successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to initialize test suppliers'
                }), 500
        except Exception as e:
            logging.error(f"Error initializing test suppliers: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    @app.route('/api/user/profile', methods=['GET'])
    @jwt_required()
    def get_user_profile():
        try:
            # Get the current user's email from JWT token
            email = get_jwt_identity()
            logging.info(f"Fetching profile for user email: {email}")
            
            # Get user ID from email
            userid = get_user_id_by_email(email)
            if not userid:
                logging.warning(f"No user found for email: {email}")
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404

            # Query the database for user profile data
            user_data = get_user_profile_by_id(userid)
            logging.info(f"Retrieved user data: {user_data}")
            
            if not user_data:
                logging.warning(f"No profile found for user ID: {userid}")
                return jsonify({
                    'status': 'error',
                    'message': 'Profile not found'
                }), 404

            # Ensure all required fields are present
            required_fields = ['first_name', 'last_name', 'email', 'contact_number', 'profile_picture_url']
            for field in required_fields:
                if field not in user_data:
                    logging.warning(f"Missing required field in user data: {field}")
                    user_data[field] = None

            response = jsonify({
                'status': 'success',
                'data': user_data
            })
            return response, 200

        except Exception as e:
            logging.error(f"Error fetching user profile: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    @app.route('/api/user/change-password', methods=['POST'])
    @jwt_required()
    def change_password_route():
        try:
            data = request.json
            current_password = data.get('current_password')
            new_password = data.get('new_password')

            if not current_password or not new_password:
                return jsonify({
                    'status': 'error',
                    'message': 'Current password and new password are required'
                }), 400

            # Get user ID from the JWT token
            email = get_jwt_identity()
            user_id = get_user_id_by_email(email)

            if not user_id:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404

            # Attempt to change password
            success, message = change_password(user_id, current_password, new_password)

            if success:
                return jsonify({
                    'status': 'success',
                    'message': message
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': message
                }), 400

        except Exception as e:
            print(f"Error in change_password_route: {e}")
            return jsonify({
                'status': 'error',
                'message': 'An error occurred while changing password'
            }), 500

    @app.route('/api/packages', methods=['GET'])
    def get_packages():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all packages with related information
            cursor.execute("""
                SELECT 
                    ep.package_id,
                    ep.package_name,
                    ep.capacity,
                    ep.description,
                    ep.additional_capacity_charges,
                    ep.charge_unit,
                    ep.total_price,
                    COALESCE(ep.status, 'active') as status,
                    v.venue_name,
                    v.location,
                    v.venue_price,
                    v.venue_capacity,
                    v.description as venue_description,
                    et.event_type_name,
                    gp.gown_package_name,
                    gp.gown_package_price,
                    gp.description as gown_package_description,
                    v.image as venue_image
                FROM event_packages ep
                LEFT JOIN venues v ON ep.venue_id = v.venue_id
                LEFT JOIN event_type et ON ep.event_type_id = et.event_type_id
                LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
                WHERE ep.status IS NULL OR LOWER(ep.status) = 'active'
                ORDER BY ep.package_id DESC
            """)
            
            packages = cursor.fetchall()
            print(f"Found {len(packages)} packages")  # Debug log
            
            # Format the results
            formatted_packages = []
            for package in packages:
                # Process venue image path
                venue_image = package[17]  # venue_image is at index 17
                if venue_image:
                    # Handle different path formats
                    if '\\' in venue_image:
                        venue_image = venue_image.split('\\')[-1]
                    elif '/' in venue_image:
                        venue_image = venue_image.split('/')[-1]
                    
                    # If the image is one of our static images, use direct static path
                    static_images = ['grandballroom.png', 'hogwarts.png', 'oceanview.png', 'paseo.png', 'sealavie.png']
                    if any(venue_image.endswith(img) for img in static_images):
                        venue_image = f'/img/venues-img/{venue_image}'
                    # For uploaded images, use API endpoint
                    else:
                        venue_image = f'/api/venue-image/{venue_image}'
                
                formatted_packages.append({
                    'package_id': package[0],
                    'package_name': package[1],
                    'capacity': package[2],
                    'description': package[3],
                    'additional_capacity_charges': float(package[4]) if package[4] else 0,
                    'charge_unit': package[5],
                    'total_price': float(package[6]) if package[6] else 0,
                    'status': package[7],
                    'venue': {
                        'name': package[8],
                        'location': package[9],
                        'price': float(package[10]) if package[10] else 0,
                        'capacity': package[11],
                        'description': package[12],
                        'image': venue_image
                    } if package[8] else None,
                    'event_type': package[13] if package[13] else None,
                    'gown_package': {
                        'name': package[14],
                        'price': float(package[15]) if package[15] else 0,
                        'description': package[16]
                    } if package[14] else None
                })
            
            cursor.close()
            conn.close()
            
            response = jsonify({
                'status': 'success',
                'data': formatted_packages
            })
            
            # Add CORS headers
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            
            return response
            
        except Exception as e:
            print(f"Error fetching packages: {str(e)}")
            response = jsonify({
                'status': 'error',
                'message': str(e)
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/api/user/profile-image/<path:filename>')
    def serve_profile_image(filename):
        """Serve profile images from the users_profile directory"""
        try:
            # Check if the requested file exists
            image_path = os.path.join('E:/eims/saved/users_profile', filename)
            if os.path.exists(image_path):
                return send_from_directory('E:/eims/saved/users_profile', filename)
            
            # If file doesn't exist, return the dummy profile pic
            return send_from_directory('E:/eims/saved/users_profile', 'dummy_profile.png')
        except Exception as e:
            logger.error(f"Error serving profile image: {e}")
            try:
                # As a last resort, try to serve the dummy profile
                return send_from_directory('E:/eims/saved/users_profile', 'dummy_profile.png')
            except:
                return jsonify({
                    'status': 'error',
                    'message': 'Image not found'
                }), 404

    @app.route('/api/user/update-profile-picture', methods=['POST'])
    @jwt_required()
    def update_profile_picture():
        try:
            if 'profile_image' not in request.files:
                return jsonify({
                    'status': 'error',
                    'message': 'No file provided'
                }), 400

            file = request.files['profile_image']
            if file.filename == '':
                return jsonify({
                    'status': 'error',
                    'message': 'No file selected'
                }), 400

            # Get current user's email from JWT
            email = get_jwt_identity()
            user_id = get_user_id_by_email(email)
            
            if not user_id:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404

            # Check if file type is allowed
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if not '.' in file.filename or \
               file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid file type'
                }), 400

            # Create a secure filename with timestamp and UUID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"profile_{user_id}_{timestamp}_{str(uuid.uuid4())[:8]}.{file_extension}"
            
            # Ensure the directory exists
            os.makedirs('E:/eims/saved/users_profile', exist_ok=True)
            
            # Save file to the specified directory
            save_path = os.path.join('E:/eims/saved/users_profile', filename)
            file.save(save_path)

            # Update user's profile picture in database
            if update_user_profile_picture(user_id, filename):
                return jsonify({
                    'status': 'success',
                    'message': 'Profile picture updated successfully',
                    'data': {
                        'image_url': filename
                    }
                }), 200
            else:
                # If database update fails, delete the uploaded file
                if os.path.exists(save_path):
                    os.remove(save_path)
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to update profile picture in database'
                }), 500

        except Exception as e:
            logger.error(f"Error updating profile picture: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    @app.after_request
    def after_request(response):
        """Add CORS headers to all responses"""
        # Set standard CORS headers
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.set('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        return response