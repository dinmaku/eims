# Supplier Availability Management Feature

## Overview
This feature allows suppliers to mark specific dates as unavailable in their calendar, preventing new bookings on those dates.

## Features Added

### Backend Changes
1. **Database Table**: `supplier_availability` table to store availability records
2. **API Endpoints**:
   - `GET /api/supplier/availability` - Fetch supplier availability
   - `POST /api/supplier/availability` - Set availability for a date
   - `DELETE /api/supplier/availability/<date>` - Remove availability record

### Frontend Changes
1. **Enhanced Sidebar**: Added toggle between "Add Event" and "Availability" modes
2. **Availability Form**: Form to mark dates as available/unavailable with optional reason
3. **Calendar Integration**: Unavailable dates appear as red events on the calendar
4. **Header Button**: Quick access to availability management

## How to Use

### For Suppliers
1. **Mark Dates as Unavailable**:
   - Click "Manage Availability" button in the header
   - Select a date
   - Choose "Unavailable" status
   - Add optional reason
   - Click "Mark as Unavailable"

2. **Mark Dates as Available**:
   - Click "Manage Availability" button
   - Select a date that was previously marked unavailable
   - Choose "Available" status
   - Click "Mark as Available"

3. **Quick Date Selection**:
   - Click directly on any date in the calendar
   - The sidebar will open with that date pre-selected

4. **Remove Unavailable Dates**:
   - Click on any red "Unavailable" event in the calendar
   - Confirm the removal in the popup dialog
   - The date will be marked as available again

5. **View Current Unavailable Dates**:
   - Open the availability sidebar
   - See a list of all currently unavailable dates
   - Click "Remove" next to any date to make it available

### Visual Indicators
- **Red Events**: Unavailable dates appear as red blocks on the calendar
- **Blue Events**: Regular booked events appear as blue blocks
- **Orange Events**: Pending events appear as orange blocks

## Database Schema

```sql
CREATE TABLE supplier_availability (
    availability_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    date DATE NOT NULL,
    is_available BOOLEAN DEFAULT true,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_supplier_availability_supplier FOREIGN KEY (supplier_id) 
        REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    CONSTRAINT unique_supplier_date UNIQUE (supplier_id, date)
);
```

## API Endpoints

### GET /api/supplier/availability
**Query Parameters:**
- `start_date` (optional): Filter from this date
- `end_date` (optional): Filter to this date

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "availability_id": 1,
      "supplier_id": 123,
      "date": "2024-01-15",
      "is_available": false,
      "reason": "Personal day off",
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

### POST /api/supplier/availability
**Request Body:**
```json
{
  "date": "2024-01-15",
  "is_available": false,
  "reason": "Personal day off"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Availability updated successfully"
}
```

### DELETE /api/supplier/availability/<date>
**Response:**
```json
{
  "status": "success",
  "message": "Availability removed successfully"
}
```

## Setup Instructions

1. **Run Database Migration**:
   ```bash
   cd eims-admin_project/eims_admin_backend
   python create_availability_table.py
   ```

2. **Restart Backend Server**:
   ```bash
   cd eims-client_project/eims_client_backend
   python app.py
   ```

3. **Test the Feature**:
   - Login as a supplier
   - Navigate to the vendor schedule page
   - Click "Manage Availability" or click on a date in the calendar
   - Mark some dates as unavailable
   - Verify they appear as red events on the calendar
   - Click on red events to remove them
   - Check the sidebar to see all unavailable dates

## Benefits
- **Prevent Double Bookings**: Suppliers can block dates they're not available
- **Better Planning**: Visual calendar shows both events and availability
- **Flexible Management**: Easy to mark dates as available/unavailable
- **Audit Trail**: All changes are tracked with timestamps
- **Reason Tracking**: Optional reasons help with communication

## Future Enhancements
- Bulk date selection for marking multiple dates at once
- Recurring availability patterns (e.g., every Monday)
- Integration with booking system to prevent conflicts
- Email notifications when availability changes
- Availability calendar export/import functionality 