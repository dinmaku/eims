<template>
    <div class="h-screen flex flex-col items-center bg-gray-200 overflow-x-hidden overflow-y-auto px-4 md:px-8">
        <!-- Alert Modal -->
        <div v-if="showAlert" class="fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto flex justify-center items-center z-[9999]">
            <div :class="['bg-white p-5 rounded-lg shadow-lg w-[400px] border-l-4', alertType === 'success' ? 'border-green-500' : 'border-red-500']">
                <div class="flex justify-between items-center mb-4">
                    <h3 :class="['text-lg font-semibold', alertType === 'success' ? 'text-green-600' : 'text-red-600']">
                        {{ alertType === 'success' ? 'Success' : 'Error' }}
                    </h3>
                    <button @click="closeAlert" class="text-gray-500 hover:text-gray-700">
                        <span class="text-2xl">&times;</span>
                    </button>
                </div>
                <p class="text-gray-700">{{ alertMessage }}</p>
                <div class="flex justify-end mt-4">
                    <button @click="closeAlert" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200">
                        Close
                    </button>
                </div>
            </div>
        </div>

        <div class="w-full mt-32">
            <div class="mt-12 md:mt-1 ml-2 md:ml-16">
                <h1 class="text-2xl md:text-4xl font-raleway font-medium text-gray-800 tracking-wide">Booking Status</h1>
                <p class="text-sm md:text-md text-gray-500">Track your outfit and event booking reservations.</p>
            </div>

            <div class="flex flex-col md:flex-row m-4 md:m-20 mt-4 md:mt-10">
              
                <div class="flex flex-col items-center w-full mt-4 md:mt-0 md:ml-16 relative">
                    <div class="w-full max-w-[950px] mx-auto">  
                        <div v-if="events_navigation" class="flex flex-wrap items-center justify-center space-x-2 md:space-x-4 bg-gray-50 px-3 md:px-5 py-2 rounded-lg shadow-lg w-full">
                            <button
                                @click="setActiveNav('wishlist')"
                                :class="{
                                    'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'wishlist',
                                    'text-gray-600': activeNavButton !== 'wishlist'
                                }"
                                class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-2"
                            >
                                Wishlist
                            </button>
                            <button
                                @click="setActiveNav('upcoming')"
                                :class="{
                                    'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'upcoming',
                                    'text-gray-600': activeNavButton !== 'upcoming'
                                }"
                                class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-2"
                            >
                                Upcoming
                            </button>
                            <button
                                @click="setActiveNav('finished')"
                                :class="{
                                    'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'finished',
                                    'text-gray-600': activeNavButton !== 'finished'
                                }"
                                class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-2"
                            >
                                Finished
                            </button>
                            <button
                                @click="setActiveNav('cancelled')"
                                :class="{
                                    'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'cancelled',
                                    'text-gray-600': activeNavButton !== 'cancelled'
                                }"
                                class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-2"
                            >
                                Cancelled
                            </button>
                            <button
                                @click="setActiveNav('all')"
                                :class="{
                                    'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'all',
                                    'text-gray-600': activeNavButton !== 'all'
                                }"
                                class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-2"
                            >
                                All
                            </button>
                        </div>

                        <div v-if="displayBookedWishlist" class="flex justify-center mt-5">
                            <div class="bg-gray-100 p-3 md:p-5 rounded-lg shadow-md overflow-x-auto w-full">
                                <table class="min-w-full border-collapse">
                                    <thead>
                                        <tr>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Name</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Type</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Theme</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Venue</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Status</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Price</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in paginatedWishlist" :key="index">
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_name }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_type }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_theme }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.venue?.venue_name || 'No venue selected' }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm">
                                                <span 
                                                    :class="{
                                                        'bg-blue-100 text-blue-800': item.event_status === 'Wishlist',
                                                        'bg-yellow-100 text-yellow-800': item.event_status === 'Upcoming',
                                                        'bg-green-100 text-green-800': item.event_status === 'Finished',
                                                        'bg-purple-100 text-purple-800': item.event_status === 'Finished',
                                                        'bg-red-100 text-red-800': item.event_status === 'Cancelled'
                                                    }"
                                                    class="px-2 py-1 rounded-full text-xs font-medium"
                                                >
                                                    {{ item.event_status }}
                                                </span>
                                            </td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ formatPrice(item.total_price) }} php</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">
                                                <button @click="displayWishlistDetails(item)" class="text-blue-500 hover:text-blue-700 mr-2">View</button>
                                                <button 
                                                    v-if="item.event_status === 'Finished'" 
                                                    @click="openRatingModal(item)"
                                                    class="text-green-500 hover:text-green-700"
                                                >
                                                    Rate
                                                </button>
                                            </td>
                                        </tr>
                                        <tr v-if="paginatedWishlist.length === 0">
                                            <td colspan="7" class="px-2 md:px-6 py-4 text-center text-sm text-gray-500">
                                                No events found in this category.
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div class="mt-4 flex justify-center items-center space-x-2">
                                    <button 
                                        @click="prevPage" 
                                        :disabled="currentPage === 1"
                                        :class="{'opacity-50 cursor-not-allowed': currentPage === 1}"
                                        class="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                                        </svg>
                                    </button>
                                    
                                    <div class="flex space-x-1">
                                        <template v-for="page in totalPages" :key="page">
                                            <button 
                                                @click="setPage(page)" 
                                                :class="[
                                                    'w-8 h-8 rounded-full text-sm font-medium transition-colors focus:outline-none',
                                                    currentPage === page 
                                                        ? 'bg-blue-500 text-white' 
                                                        : 'text-gray-700 hover:bg-blue-100'
                                                ]"
                                            >
                                                {{ page }}
                                            </button>
                                        </template>
                                    </div>
                                    
                                    <button 
                                        @click="nextPage" 
                                        :disabled="currentPage >= totalPages"
                                        :class="{'opacity-50 cursor-not-allowed': currentPage >= totalPages}"
                                        class="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


   <!-- Modal for selected wishlist details -->
<div v-if="selectedWishlist" @click.self="closeWishlistModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white p-4 md:p-6 rounded-xl shadow-lg w-full max-w-[95%] md:max-w-[700px] overflow-y-auto max-h-[90vh]">
        <button @click="closeWishlistModal" class="text-gray-500 text-2xl md:text-3xl float-right">&times;</button>
        <div class="mt-3 md:mt-5">
            <h1 class="text-lg md:text-xl font-bold mb-3 md:mb-4 font-raleway">Wishlist Details</h1>
            <div class="flex flex-col space-y-4">
                <p class="text-gray-600">Event Name: <span class="text-black">{{ selectedWishlist.event_name }}</span></p>
                <div class="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
                    <div class="bg-gray-300 w-full md:w-1/2 px-2 py-3 space-y-2 rounded-xl">
                        <p class="text-gray-700">Event Type</p>
                        <p>{{ selectedWishlist.event_type }}</p>
                    </div>
                    <div class="bg-gray-300 w-full md:w-1/2 px-2 py-3 space-y-2 rounded-xl">
                        <p class="text-gray-700">Event Theme</p>
                        <p>{{ selectedWishlist.event_theme }}</p>
                    </div>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Event Color</p>
                    <p>{{ selectedWishlist.event_color }}</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Schedule Details</p>
                    <p>Date: {{ selectedWishlist.schedule || 'Not set' }}</p>
                    <p>Start Time: {{ selectedWishlist.start_time || 'Not set' }}</p>
                    <p>End Time: {{ selectedWishlist.end_time || 'Not set' }}</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Venue</p>
                    <p>{{ selectedWishlist.venue?.venue_name || 'No venue selected' }}</p>
                    <p class="text-sm text-gray-600">Location: {{ selectedWishlist.venue?.location || 'N/A' }}</p>
                    <p class="text-sm text-gray-600">Price: {{ formatPrice(selectedWishlist.venue?.venue_price) || 'N/A' }} php</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Package Details</p>
                    <p>Name: {{ selectedWishlist.package_name }}</p>
                    <p>Capacity: {{ selectedWishlist.capacity }} persons</p>
                    <p v-if="selectedWishlist.additional_capacity_charges">Additional Charges: {{ formatPrice(selectedWishlist.additional_capacity_charges) }} php per {{ selectedWishlist.charge_unit }} person(s)</p>
                    <p class="mt-2">Status: <span :class="{'text-green-600': selectedWishlist.package_status === 'Active', 'text-yellow-600': selectedWishlist.package_status === 'Pending', 'text-red-600': selectedWishlist.package_status === 'Cancelled'}">{{ selectedWishlist.package_status }}</span></p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Total Price</p>
                    <p>{{ formatPrice(selectedWishlist.total_price) }} php</p>
                </div>
           
                <!-- Section for Suppliers -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Suppliers</p>
                    <button @click="showSuppliers = !showSuppliers" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {{ showSuppliers ? 'Hide Suppliers' : 'Show Suppliers' }}
                    </button>
                    <div v-if="showSuppliers" class="mt-2 overflow-y-auto max-h-64 space-y-2">
                        <div v-if="selectedWishlist.suppliers && selectedWishlist.suppliers.length > 0">
                            <div v-for="supplier in selectedWishlist.suppliers" :key="supplier.supplier_id" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                                <p class="font-semibold text-gray-800">{{ supplier.name }}</p>
                                <p class="text-gray-600">Service: {{ supplier.service }}</p>
                                <p class="text-gray-600">Price: {{ formatPrice(supplier.price) }} php</p>
                                <p class="text-gray-600">Status: <span :class="{'text-green-600': supplier.status === 'Active', 'text-yellow-600': supplier.status === 'Pending', 'text-red-600': supplier.status === 'Cancelled'}">{{ supplier.status }}</span></p>
                                <p v-if="supplier.remarks" class="text-gray-600">Remarks: {{ supplier.remarks }}</p>
                            </div>
                        </div>
                        <p v-else class="text-gray-600">No suppliers selected</p>
                    </div>
                </div>

                <!-- Section for Outfit Package -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl mt-4">
                    <p class="text-gray-700 font-semibold">Outfit Package</p>
                    <div class="space-y-2">
                        <div v-if="selectedWishlist.gown_package_name">
                            <p class="text-sm">Package Name: {{ selectedWishlist.gown_package_name }}</p>
                            <p class="text-sm">Package Price: {{ formatPrice(selectedWishlist.gown_package_price) }} php</p>
                        </div>
                        
                        <!-- Outfits Table -->
                        <div class="mt-4" v-if="selectedWishlist.outfits && selectedWishlist.outfits.length > 0">
                            <p class="text-sm font-medium mb-2">{{ selectedWishlist.gown_package_name ? 'Included Outfits:' : 'Selected Outfits:' }}</p>
                            <div class="overflow-x-auto">
                                <table class="min-w-full bg-white rounded-lg overflow-hidden">
                                    <thead class="bg-gray-100">
                                        <tr>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Name</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Type</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Color</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Price</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Status</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-gray-200">
                                        <tr v-for="outfit in selectedWishlist.outfits" :key="outfit.outfit_id" class="hover:bg-gray-50">
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_name }}</td>
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_type }}</td>
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_color }}</td>
                                            <td class="px-4 py-2 text-sm">{{ formatPrice(outfit.rent_price) }} php</td>
                                            <td class="px-4 py-2 text-sm">
                                                <span :class="{'text-green-600': outfit.status === 'Active', 'text-yellow-600': outfit.status === 'Pending', 'text-red-600': outfit.status === 'Cancelled'}">
                                                    {{ outfit.status }}
                                                </span>
                                            </td>
                                            <td class="px-4 py-2 text-sm">
                                                <button 
                                                    @click="viewOutfitImage(outfit)"
                                                    class="text-blue-500 hover:text-blue-700"
                                                >
                                                    View Image
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div v-else class="text-gray-600 text-sm">No outfits available.</div>
                    </div>
                </div>

                <!-- Section for Additional Services -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl mt-4">
                    <p class="text-gray-700 font-semibold">Additional Services</p>
                    <button @click="showAdditionalServices = !showAdditionalServices" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {{ showAdditionalServices ? 'Hide Services' : 'Show Services' }}
                    </button>
                    
                    <div v-if="showAdditionalServices" class="mt-2 overflow-y-auto max-h-64 space-y-2">
                        <div v-if="selectedWishlist.additional_services && selectedWishlist.additional_services.length > 0">
                            <div v-for="service in selectedWishlist.additional_services" :key="service.add_service_id" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                                <p class="font-semibold text-gray-800">{{ service.add_service_name }}</p>
                                <p class="text-gray-600">{{ service.add_service_description }}</p>
                                <p class="text-gray-600">Price: {{ formatPrice(service.add_service_price) }} php</p>
                                <p class="text-gray-600">Status: <span :class="{'text-green-600': service.status === 'Active', 'text-yellow-600': service.status === 'Pending', 'text-red-600': service.status === 'Cancelled'}">{{ service.status }}</span></p>
                                <p v-if="service.remarks" class="text-gray-600">Remarks: {{ service.remarks }}</p>
                            </div>
                        </div>
                        <p v-else class="text-gray-600">No additional services selected</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>



        <!-- Outfit Image Modal -->
        <div 
            v-if="selectedOutfit" 
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            @click.self="selectedOutfit = null"
        >
            <div class="bg-white p-4 rounded-lg max-w-xl w-full mx-4">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold">{{ selectedOutfit.outfit_name }}</h3>
                    <button @click="selectedOutfit = null" class="text-gray-500 hover:text-gray-700">
                        <span class="text-2xl">&times;</span>
                    </button>
                </div>
                <div class="flex justify-center">
                    <img 
                        :src="getOutfitImageUrl(selectedOutfit.outfit_img)" 
                        :alt="selectedOutfit.outfit_name" 
                        @error="handleImageError"
                        class="w-auto h-[400px] object-contain rounded-lg"
                    >
                </div>
                <div class="mt-4 text-sm text-gray-600">
                    <p><span class="font-medium">Type:</span> {{ selectedOutfit.outfit_type }}</p>
                    <p><span class="font-medium">Color:</span> {{ selectedOutfit.outfit_color }}</p>
                    <p v-if="selectedOutfit.outfit_desc"><span class="font-medium">Description:</span> {{ selectedOutfit.outfit_desc }}</p>
                    <p><span class="font-medium">Status:</span> <span :class="{'text-green-600': selectedOutfit.status === 'Active', 'text-yellow-600': selectedOutfit.status === 'Pending', 'text-red-600': selectedOutfit.status === 'Cancelled'}">{{ selectedOutfit.status }}</span></p>
                    <p v-if="selectedOutfit.remarks"><span class="font-medium">Remarks:</span> {{ selectedOutfit.remarks }}</p>
                </div>
            </div>
        </div>




       
   


    </div>

    <!-- Rating Modal -->
    <div v-if="showRatingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">Rate Your Event Experience</h3>
                <button @click="closeRatingModal" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <div class="mb-6">
                <p class="text-gray-600 mb-2">Event: {{ selectedEventForRating?.event_name }}</p>
                <div class="flex items-center space-x-2 mb-4">
                    <span class="text-gray-700">Rating:</span>
                    <div class="flex space-x-1">
                        <button 
                            v-for="star in 5" 
                            :key="star"
                            @click="setRating(star)"
                            class="text-2xl focus:outline-none"
                            :class="star <= rating ? 'text-yellow-400' : 'text-gray-300'"
                        >
                            ★
                        </button>
                    </div>
                </div>
                
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Feedback (Optional)</label>
                    <textarea 
                        v-model="feedbackText"
                        class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows="4"
                        placeholder="Share your experience..."
                    ></textarea>
                </div>
            </div>

            <div class="flex justify-end space-x-3">
                <button 
                    @click="closeRatingModal"
                    class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg"
                >
                    Cancel
                </button>
                <button 
                    @click="submitRating"
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                    :disabled="!rating"
                >
                    Submit Rating
                </button>
            </div>
        </div>
    </div>

    <!-- View Feedback Modal -->
    <div v-if="showViewFeedbackModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">Your Event Feedback</h3>
                <button @click="closeRatingModal" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
            </div>
            
            <div class="mb-6">
                <p class="text-gray-600 mb-2">Event: {{ selectedEventForRating?.event_name }}</p>
                <div class="flex items-center space-x-2 mb-4">
                    <span class="text-gray-700">Your Rating:</span>
                    <div class="flex space-x-1">
                        <span 
                            v-for="star in 5" 
                            :key="star"
                            class="text-2xl"
                            :class="star <= (existingFeedback?.rating || 0) ? 'text-yellow-400' : 'text-gray-300'"
                        >
                            ★
                        </span>
                    </div>
                </div>
                
                <div class="mb-4">
                    <p class="text-gray-700 mb-2">Your Feedback:</p>
                    <p class="px-3 py-2 bg-gray-100 rounded-lg">
                        {{ existingFeedback?.feedback_text || 'No written feedback provided.' }}
                    </p>
                </div>

                <div class="text-sm text-gray-500 mt-4">
                    Submitted on: {{ existingFeedback?.created_at ? new Date(existingFeedback.created_at).toLocaleString() : 'N/A' }}
                </div>
            </div>

            <div class="flex justify-end">
                <button 
                    @click="closeRatingModal"
                    class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
                >
                    Close
                </button>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';

interface Venue {
    venue_id: number;
    venue_name: string;
    location: string;
    venue_price: number;
    description: string;
    venue_capacity: number;
    status: string;
    remarks: string;
}

interface BookedEvent {
    events_id: number;
    event_name: string;
    event_type: string;
    event_theme: string;
    event_color: string;
    schedule: string;
    start_time: string;
    end_time: string;
    event_status: string;
    total_price: number;
    venue?: Venue;
    outfits: any[];
    suppliers: any[];
    additional_services: any[];
    gown_package_name?: string;
    gown_package_price?: number;
    package_name?: string;
    capacity?: number;
    description?: string;
    additional_capacity_charges?: number;
    charge_unit?: number;
    package_status?: string;
}

interface Feedback {
    feedback_id: number;
    rating: number;
    feedback_text: string;
    created_at: string;
    user_firstname: string;
    user_lastname: string;
}

interface Outfit {
    outfit_id: number;
    outfit_name: string;
    outfit_type: string;
    outfit_color: string;
    outfit_desc: string;
    outfit_img: string;
    rent_price: number;
    status: string;
    remarks?: string;
}

export default defineComponent({
    name: 'BookedServices',
    data() {
        return {
            events_navigation: true,
            selectedWishlist: null as BookedEvent | null,
            selectedOutfit: null as Outfit | null,
            activeNavButton: 'wishlist' as 'wishlist' | 'upcoming' | 'finished' | 'cancelled' | 'all',
            
            // Pagination
            currentPage: 1,
            itemsPerPage: 3,
            
            // Display flags
            displayWishlist: true,
            displayUpcoming: false,
            displayFinished: false,
            displayCancelled: false,
            displayAll: false,
            displayBookedWishlist: true,
            displayBookedOutfits: false,

            // Data arrays
            bookedWishlist: [] as BookedEvent[],
            bookedOutfits: [] as Outfit[],

            // Modal toggles
            showSuppliers: false,
            showAdditionalServices: false,
            showRatingModal: false,
            showViewFeedbackModal: false,
            selectedEventForRating: null as BookedEvent | null,
            rating: 0,
            feedbackText: '',
            existingFeedback: null as Feedback | null,
            showAlert: false,
            alertType: 'success',
            alertMessage: '',
        };
    },
    computed: {
        filteredWishlist() {
            if (!this.bookedWishlist) return [];
            
            let filtered;
            switch (this.activeNavButton) {
                case 'wishlist':
                    filtered = this.bookedWishlist.filter(item => item.event_status === 'Wishlist');
                    break;
                case 'upcoming':
                    filtered = this.bookedWishlist.filter(item => item.event_status === 'Upcoming');
                    break;
                case 'finished':
                    filtered = this.bookedWishlist.filter(item => item.event_status === 'Finished');
                    break;
                case 'cancelled':
                    filtered = this.bookedWishlist.filter(item => item.event_status === 'Cancelled');
                    break;
                case 'all':
                default:
                    filtered = this.bookedWishlist;
            }
            
            return filtered;
        },
        
        // Add paginated wishlist
        paginatedWishlist() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            return this.filteredWishlist.slice(startIndex, endIndex);
        },
        
        // Total pages
        totalPages() {
            return Math.ceil(this.filteredWishlist.length / this.itemsPerPage);
        }
    },
    created() {
        this.fetchBookedWishlist();
        this.fetchBookedOutfits();
    },
    methods: {
        setActiveNav(type: 'wishlist' | 'upcoming' | 'finished' | 'cancelled' | 'all') {
            this.activeNavButton = type;
            // Reset all display flags
            this.displayWishlist = false;
            this.displayUpcoming = false;
            this.displayFinished = false;
            this.displayCancelled = false;
            this.displayAll = false;

            // Set the appropriate display flag
            switch (type) {
                case 'wishlist':
                    this.displayWishlist = true;
                    break;
                case 'upcoming':
                    this.displayUpcoming = true;
                    break;
                case 'finished':
                    this.displayFinished = true;
                    break;
                case 'cancelled':
                    this.displayCancelled = true;
                    break;
                case 'all':
                    this.displayAll = true;
                    break;
            }
        },
        
        toggleWishlistDisplay() {
            this.displayBookedWishlist = true;
        },
        
        displayEventSection() {
            this.displayBookedWishlist = true;
            this.events_navigation = true;
            this.displayBookedOutfits = false;
        },
        
        displayOutfitsSection() {
            this.displayBookedWishlist = false;
            this.events_navigation = false;
            this.displayBookedOutfits = true;
        },

        formatPrice(price) {
            if (price === null || price === undefined || isNaN(price)) {
                return 'N/A'; // Return a fallback if price is invalid
            }
            // Round the price to 2 decimal places and format with commas
            return parseFloat(price).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        },

        async fetchBookedWishlist() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.get('http://127.0.0.1:5001/wishlist', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                });
                
                console.log('Received wishlist data:', response.data);
                this.bookedWishlist = response.data;
                // Reset to page 1 when data changes
                this.currentPage = 1;
            } catch (error) {
                console.error('Error fetching booked wishlist:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else if (error.response?.status === 422) {
                    // Invalid data format
                    console.error('Invalid data format:', error.response.data);
                }
            }
        },

        async deleteWishlistItem(events_id) {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.delete(`http://127.0.0.1:5001/booked_wishlist/${events_id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.status === 200) {
                    this.bookedWishlist = this.bookedWishlist.filter(item => item.events_id !== events_id);
                    alert('Event item deleted successfully!');
                    this.selectedWishlist = null;  // Changed from false to null to match the data type
                    this.closeWishlistModal();
                }
            } catch (error) {
                console.error('Error deleting event item:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else {
                    alert('Failed to delete event item. Please try again.');
                }
            }
        },

        displayWishlistDetails(item) {
            console.log('Selected wishlist item:', item);
            console.log('Gown package name:', item.gown_package_name);
            console.log('Gown package price:', item.gown_package_price);
            console.log('Outfits array:', item.outfits);
            
            // Ensure outfits are properly formatted
            if (item.outfits && Array.isArray(item.outfits)) {
                console.log('Number of outfits:', item.outfits.length);
                item.outfits.forEach((outfit, index) => {
                    console.log(`Outfit ${index + 1}:`, outfit);
                });
                this.selectedWishlist = item;
            } else {
                console.warn('No valid outfits array found, creating empty array');
                this.selectedWishlist = {
                    ...item,
                    outfits: []
                };
            }
        },
        closeWishlistModal() {
            this.selectedWishlist = null;
            this.showSuppliers = false;
            this.showAdditionalServices = false;
        },

        async fetchBookedOutfits() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.get('http://127.0.0.1:5001/booked-outfits', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                });
                this.bookedOutfits = response.data;
            } catch (error) {
                console.error('Error fetching booked outfits:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else if (error.response?.status === 422) {
                    // Invalid data format
                    console.error('Invalid data format:', error.response.data);
                }
            }
        },
        viewOutfitImage(outfit) {
            if (outfit && outfit.outfit_img) {
                this.selectedOutfit = outfit;
            } else {
                alert('No image available for this outfit.');
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        setPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
        async openRatingModal(event) {
            try {
                // First check if user has already rated this event
                const token = localStorage.getItem('access_token');
                const response = await axios.get(`http://127.0.0.1:5001/event-feedback/${event.events_id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.data.data && response.data.data.length > 0) {
                    // User has already rated, show the feedback
                    this.existingFeedback = response.data.data[0]; // Get the first feedback (should be user's own)
                    this.selectedEventForRating = event;
                    this.showViewFeedbackModal = true;
                } else {
                    // User hasn't rated yet, show rating modal
                    this.selectedEventForRating = event;
                    this.showRatingModal = true;
                    this.rating = 0;
                    this.feedbackText = '';
                }
            } catch (error) {
                console.error('Error checking feedback:', error);
                alert('Error checking feedback status');
            }
        },

        closeRatingModal() {
            this.showRatingModal = false;
            this.showViewFeedbackModal = false;
            this.selectedEventForRating = null;
            this.rating = 0;
            this.feedbackText = '';
            this.existingFeedback = null;
        },

        setRating(value) {
            this.rating = value;
        },

        async submitRating() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.post('http://127.0.0.1:5001/event-feedback', {
                    events_id: this.selectedEventForRating.events_id,
                    rating: this.rating,
                    feedback_text: this.feedbackText
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.status === 201) {
                    this.showAlertMessage('success', 'Thank you for your feedback!');
                    this.closeRatingModal();
                }
            } catch (error) {
                console.error('Error submitting rating:', error);
                if (error.response?.status === 401) {
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else if (error.response?.status === 409) {
                    this.showAlertMessage('error', 'You have already submitted feedback for this event.');
                } else {
                    this.showAlertMessage('error', 'Failed to submit rating. Please try again.');
                }
            }
        },

        getOutfitImageUrl(imageFileName) {
            if (!imageFileName) {
                return `http://127.0.0.1:5001/api/outfits/image/default_outfit.png`;
            }
            // Clean up the image filename to only use the actual filename
            const filename = imageFileName.split(/[\/\\]/).pop();
            return `http://127.0.0.1:5001/api/outfits/image/${filename}`;
        },

        handleImageError(e) {
            e.target.style.display = 'none';
        },

        showAlertMessage(type: 'success' | 'error', message: string) {
            this.alertType = type;
            this.alertMessage = message;
            this.showAlert = true;
        },

        closeAlert() {
            this.showAlert = false;
            this.alertMessage = '';
        },
    },

    mounted() {
        this.fetchBookedWishlist();
        this.fetchBookedOutfits();  // Automatically call the function when the component is mounted
    },
})
</script>

<style scoped>
</style>