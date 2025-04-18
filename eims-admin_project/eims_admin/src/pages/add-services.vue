    <template>
    <div class="bg-gray-200 w-full h-full">
        <div class="w-full h-[65px] bg-gray-100 mt-2 flex items-center justify-between px-5 shadow-lg">
            <h1 class="font-amaticBold font-extraLight text-3xl">
                Events Packages
            </h1>
            <button class="bg-[#9B111E] font-semibold text-white px-3 py-1 rounded shadow-lg 
              transition-transform duration-300 transform hover:scale-105" @click="displayEventTypeBtn">Event Type</button>
        </div>
        
        <div class="flex flex-row items-center m-5 space-x-5">
            <div class="flex justify-start w-52 h-20 bg-white rounded-lg shadow-lg px-2 items-center border-l-2 border-green-400 space-x-5">
                <h2 class="font-amaticRegular text-4xl font-bold mb-0"> {{ totalPackages }} <span class = "text-sm antialiased text-gray-600">packages</span></h2>
            </div>
        </div>
        
        <div class="flex flex-row justify-end items-center m-5 my-7">
        <div class = "flex">
        <button class = "mr-2 w-44 h-10 bg-[#9B111E] font-semibold text-gray-100 font-quicksand rounded-md shadow-lg 
        transition-transform duration-300 transform hover:scale-105" @click="addPackagesBtn">
        Create Event Package
        </button>
        </div>
        </div>
        
        <div v-if="showTable === 'packages'" class="relative shadow-md sm:rounded-xl w-full max-w-[1170px] h-auto ml-5 mt-2 font-amaticBold mb-10">
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 table-fixed">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="w-16 px-2 py-3">#</th>
                        <th scope="col" class="w-52 px-2 py-3">Package Name</th>
                        <th scope="col" class="w-40 px-2 py-3">Package Type</th>
                        <th scope="col" class="w-52 px-2 py-3">Venue</th>
                        <th scope="col" class="w-36 px-2 py-3">Rate</th>
                        <th scope="col" class="w-28 px-2 py-3">Capacity</th>
                        <th scope="col" class="w-28 px-2 py-3">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="(packageItem, index) in paginatedPackages"
                        :key="packageItem.packageId"
                        class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800">
                        <th scope="row" class="w-16 px-2 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ packageItem.dummyIndex }}</th>
                        <td class="w-52 px-2 py-3 truncate">{{ packageItem.package_name }}</td>
                        <td class="w-40 px-2 py-3 truncate">{{ getEventTypeName(packageItem.event_type_id) }}</td>
                        <td class="w-52 px-2 py-3 truncate">{{ packageItem.venue_name }}</td>
                        <td class="w-36 px-2 py-3 truncate">{{ formatPrice(packageItem.total_price) }} php</td>
                        <td class="w-28 px-2 py-3 truncate">{{ packageItem.capacity }}</td>
                        <td class="w-28 px-2 py-3">
                            <button
                                class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
                                @click="editPackageBtn(index)"> 
                                <img src="/img/update3.png" alt="Update" class="w-5 h-5">
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <!-- Pagination Controls -->
            <div class="flex justify-center space-x-2 mt-4 mb-6">
                <button 
                    @click="prevPackagesPage" 
                    :disabled="currentPackagesPage === 1" 
                    class="px-3 py-1 bg-[#9B111E] text-white rounded-md hover:bg-[#B73A45] disabled:opacity-50 text-sm">
                    Previous
                </button>
                <button 
                    v-for="page in totalPackagesPages" 
                    :key="page" 
                    @click="changePackagesPage(page)" 
                    :class="{'bg-[#9B111E]': currentPackagesPage === page, 'bg-gray-300': currentPackagesPage !== page}" 
                    class="px-3 py-1 text-white rounded-md hover:bg-[#B73A45] text-xs">
                    {{ page }}
                </button>
                <button 
                    @click="nextPackagesPage" 
                    :disabled="currentPackagesPage === totalPackagesPages" 
                    class="px-3 py-1 bg-[#9B111E] text-white rounded-md hover:bg-[#B73A45] disabled:opacity-50 text-xs">
                    Next
                </button>
                </div>
            </div>
        </div>


        
      <!-- Add Packages Form -->
      <form v-if="addPackagesForm" @submit.prevent="addPackages" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto" @click.self="closePackagesForm">
        <div class="bg-white w-[800px] p-5 rounded-lg shadow-lg overflow-y-auto max-h-[90vh]">
          <div class="flex justify-between items-center mb-5">
            <h1 class="font-semibold text-xl text-gray-800">Add Package</h1>
          </div>

          <div class="border-b border-gray-300 mb-5"></div>

          <!-- Package Details -->
          <div>
            <h2 class="font-semibold text-lg text-gray-800 mb-4">Package Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Package Name</label>
                <input type="text" v-model="packageData.package_name" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Package Name" required />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Event Type</label>
                <select v-model="packageData.event_type_id" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200">
                  <option disabled value="">Select Event Type</option>
                  <option v-for="type in eventTypes" :key="type.event_type_id" :value="type.event_type_id">
                    {{ type.event_type_name }}
                  </option>
                  <option value="add-new">+ Add New Event Type</option>
                </select>
              </div>

              <div>
                <label for="charge_unit" class="block text-xs font-medium text-gray-700 mb-1 text-left">Unit for Additional Charges</label>
              <input type="number" id="charge_unit" v-model="packageData.charge_unit" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Set person unit" required />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Additional Capacity Charges</label>
                <input type="number" v-model="packageData.additional_capacity_charges" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Additional Capacity Charges" required />
              </div>
            </div>

            <div class="mt-5">
              <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Capacity</label>
              <input type="number" v-model="packageData.capacity" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Set Capacity" required />
            </div>

            <div class="mt-5">
              <label for="description" class="block text-xs font-medium text-gray-700 mb-1 text-left">Description</label>
              <textarea v-model="packageData.description" class="p-2 w-full h-24 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200 resize-none" placeholder="Description" required></textarea>
            </div>
          </div>
          <!-- Add New Event Type Modal -->
          <!-- Inclusion Buttons -->
          <div class="grid grid-cols-4 gap-4 mb-4">
            <button 
              @click.prevent="openInclusionModal('supplier')" 
              class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
            >
              <img alt="Supplier Icon" class="mr-2 w-[20px] h-[20px]" src="/img/supplier.png">
              Suppliers
            </button>
            <button 
              @click.prevent="openInclusionModal('venue')" 
              class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
            >
              <img alt="Venue Icon" class="mr-2 w-[20px] h-[20px]" src="/img/venues1.png">
             Venue
            </button>
            <button 
              @click.prevent="openInclusionModal('outfit')" 
              class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
            >
              <img alt="Outfit Icon" class="mr-2 w-[20px] h-[20px]" src="/img/costume.png">
             Outfit Package
            </button>
            <button 
              @click.prevent="openInclusionModal('service')" 
              class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
            >
              <img alt="Service Icon" class="mr-2 w-[20px] h-[20px]" src="/img/additionals.png">
              Inclusions
            </button>
          </div>

      <!-- Inclusion Modal for Selecting Supplier Type -->
      <div v-if="showInclusionModal && selectedInclusionType === 'supplier'" @click.self="closeInclusionModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white w-[500px] p-6 rounded-lg shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold">Select Supplier Type</h2>
            <button @click="closeInclusionModal" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="grid grid-cols-1 gap-2">
            <button v-for="serviceType in supplierTypes" :key="serviceType" @click="selectSupplierType(serviceType)" class="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md transition duration-150">
              {{ serviceType }}
            </button>
          </div>
        </div>
      </div>

      <!-- Inclusion Modal for Selecting Specific Supplier -->
      <div v-if="showSupplierModal" @click.self="closeSupplierModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white w-[500px] p-6 rounded-lg shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold">Select Supplier</h2>
            <button @click="closeSupplierModal" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div>
            <label for="supplier" class="block text-sm font-medium text-gray-700">Select Supplier</label>
            <select v-model="selectedSupplier" class="w-full p-2 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200">
              <option selected disabled value="">Select {{ selectedSupplierType }}</option>
              <option v-for="supplier in filteredSuppliers(selectedSupplierType)" :key="supplier.supplier_id" :value="supplier">
                {{ supplier.firstname }} {{ supplier.lastname }}
              </option>
            </select>
          </div>
          <div class="flex justify-center mt-4">
            <button type="button" @click="addSelectedSupplier" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Add</button>
          </div>
        </div>
      </div>

      <!-- Inclusion Modal for Selecting Venue -->
      <div v-if="showVenueModal" @click.self="closeVenueModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white w-[500px] p-6 rounded-lg shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold">Select Venue</h2>
            <button @click="closeVenueModal" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div>
            <label for="venue" class="block text-sm font-medium text-gray-700">Select Venue</label>
            <div v-if="venues && venues.length > 0">
              <select v-model="selectedVenue" class="w-full p-2 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200">
                <option selected disabled value="">Select Venue</option>
                <option v-for="venue in venues" :key="venue.venue_id" :value="venue">
                  {{ venue.venue_name }} ({{ venue.location }}) - {{ formatPrice(venue.venue_price) }}
                </option>
              </select>
            </div>
            <div v-else>
              <div class="text-red-500">No active venues available</div>
              <pre class="text-xs mt-2">{{ JSON.stringify(venues, null, 2) }}</pre>
            </div>
          </div>
          <div class="flex justify-center mt-4">
            <button type="button" @click="addSelectedVenue" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Add</button>
          </div>
        </div>
      </div>

      <!-- Inclusion Modal for Selecting Outfit Package -->
      <div v-if="showOutfitModal" @click.self="closeOutfitModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white w-[500px] p-6 rounded-lg shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold">Select Outfit Package</h2>
            <button @click="closeOutfitModal" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div>
            <label for="outfit" class="block text-sm font-medium text-gray-700">Select Outfit Package</label>
            <select v-model="selectedOutfit" class="w-full p-2 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200">
              <option selected disabled value="">Select Outfit Package</option>
              <option v-for="gownPackage in gownPackages" :key="gownPackage.gown_package_id" :value="gownPackage">
                {{ gownPackage.gown_package_name }} - {{ formatPrice(gownPackage.gown_package_price) }} php
              </option>
            </select>
          </div>
          <div class="flex justify-center mt-4">
            <button type="button" @click="addSelectedOutfit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Add</button>
          </div>
        </div>
      </div>

      <!-- Inclusion Modal for Selecting Additional Services -->
        <div v-if="showServiceModal" @click.self="closeServiceModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div class="bg-white w-[500px] p-6 rounded-lg shadow-lg">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-semibold">Select Additional Service</h2>
              <button @click="closeServiceModal" class="text-red-500 hover:text-red-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div>
              <label for="service" class="block text-sm font-medium text-gray-700">Select Additional Service</label>
              <select v-model="selectedService" class="w-full p-2 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200">
                <option selected disabled value="">Select Additional Service</option>
                <option v-for="service in filteredAdditionalServices" :key="service.add_service_id" :value="service">
                  {{ service.add_service_name }}
                </option>
              </select>
            </div>
            <div class="flex justify-center mt-4">
              <button type="button" @click="addSelectedService" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Add</button>
            </div>
          </div>
        </div>




      <!-- Inclusion Table -->
      <div class="overflow-x-auto">
        <table class="w-full table-auto border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2 text-left">Type</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Details</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Rate</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(inclusion, index) in inclusions" :key="index" class="border border-gray-300">
              <td class="border border-gray-300 px-4 py-2 capitalize">
                {{ inclusion.type === 'supplier' ? `Supplier(${inclusion.serviceType})` : inclusion.type }}
              </td>
              <td class="border border-gray-300 px-4 py-2">{{ getInclusionName(inclusion) }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ getInclusionPrice(inclusion) }}</td>
              <td class="border border-gray-300 py-2">
                <div @click="removeInclusion(index)" class="inline-block cursor-pointer">
                  <img 
                    alt="Delete Icon" 
                    class="w-[20px] h-[20px] transition-transform transform hover:scale-110 hover:brightness-90" 
                    src="/img/delete.png" 
                  >
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="mt-4 p-4 bg-gray-50 rounded-lg shadow-sm">
          <div class="flex justify-between items-center">
            <div class="text-lg font-semibold text-gray-700">Total Package Rate:</div>
            <div class="text-xl font-bold text-blue-600">{{ formatPrice(
              inclusions.reduce((total, inc) => {
                if (inc.type === 'supplier' && inc.data) total += Number(inc.data.price || 0);
                if (inc.type === 'venue' && inc.data) total += Number(inc.data.venue_price || 0);
                if (inc.type === 'outfit' && inc.data) total += Number(inc.data.gown_package_price || 0);
                if (inc.type === 'service' && inc.data) total += Number(inc.data.add_service_price || 0);
                return total;
              }, 0)
            ) }}</div>
          </div>
          <div class="mt-2 text-sm text-gray-500">
            * Rate includes all selected inclusions (suppliers, services, venue, and outfit package)
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="flex justify-center mt-8 space-x-3">
        <button class="bg-gray-300 text-white px-3 py-1 rounded hover:bg-gray-400" @click="closePackagesForm">Cancel</button>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Save</button>
      </div>
    </div>
  </form>

  <!-- Add New Event Type Modal -->
  <div
    v-if="showAddEventTypeModal"
    @click.self="closeAddEventTypeModal"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <div class="bg-white rounded-lg shadow-lg w-[400px] p-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Add New Event Type</h2>
      <input
        v-model="newEventTypeName"
        type="text"
        class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200"
        placeholder="Enter Event Type Name"
      />
      <div class="flex justify-end mt-4 space-x-2">
        <button
          @click="closeAddEventTypeModal"
          class="px-4 py-2 text-gray-700 bg-gray-300 rounded-md hover:bg-gray-400 mr-2"
        >
          Cancel
        </button>
        <button
          @click="saveNewEventType"
          class="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600"
        >
          Save
        </button>
      </div>
    </div>
  </div>

  <!-- Edit Packages Form -->
  <form v-if="editPackagesForm" @submit.prevent="confirmEditPackage" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto" @click.self="closeEditPackagesBtn">
    <div class="bg-white w-[800px] p-5 rounded-lg shadow-lg overflow-y-auto max-h-[90vh]">
      <div class="flex justify-between items-center mb-5">
        <h1 class="font-semibold text-xl text-gray-800">Update Package</h1>
      </div>

      <div class="border-b border-gray-300 mb-5"></div>

      <!-- Package Details -->
      <div>
        <h2 class="font-semibold text-lg text-gray-800 mb-4">Package Details</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Package Name</label>
            <input type="text" v-model="selectedPackage.package_name" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Package Name" required />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Package Type</label>
            <select v-model="selectedPackage.event_type_id" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" required>
              <option disabled value="">Select Event Type</option>
              <option v-for="type in eventTypes" :key="type.event_type_id" :value="type.event_type_id">
                {{ type.event_type_name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Capacity</label>
            <input type="number" v-model="selectedPackage.capacity" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Set Capacity" required />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1 text-left">Total Rate</label>
            <input type="number" v-model="selectedPackage.total_price" class="p-2 w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200" placeholder="Total Price" required />
          </div>
        </div>

        <div class="mt-5">
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea v-model="selectedPackage.description" class="p-2 w-full h-24 rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-200 resize-none" placeholder="Description" required></textarea>
        </div>
      </div>
      <!-- Inclusion Buttons -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <button 
          @click.prevent="openInclusionModal('supplier')" 
          class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
        >
          <img alt="Supplier Icon" class="mr-2 w-[20px] h-[20px]" src="/img/supplier.png">
          Suppliers
        </button>
        <button 
          @click.prevent="openInclusionModal('venue')" 
          class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
        >
          <img alt="Venue Icon" class="mr-2 w-[20px] h-[20px]" src="/img/venues1.png">
         Venue
        </button>
        <button 
          @click.prevent="openInclusionModal('outfit')" 
          class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
        >
          <img alt="Outfit Icon" class="mr-2 w-[20px] h-[20px]" src="/img/costume.png">
         Outfit Package
        </button>
        <button 
          @click.prevent="openInclusionModal('service')" 
          class="flex items-center justify-center bg-[#9B111E] text-white px-3 py-2 h-[50px] rounded-md hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
        >
          <img alt="Service Icon" class="mr-2 w-[20px] h-[20px]" src="/img/additionals.png">
          Inclusions
        </button>
      </div>

      <!-- Inclusions Table -->
      <div class="overflow-x-auto">
        <table class="w-full table-auto border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2 text-left">Type</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Details</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Price</th>
              <th class="border border-gray-300 px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(inclusion, index) in selectedPackage.inclusions" :key="index" class="border border-gray-300">
              <td class="border border-gray-300 px-4 py-2 capitalize">
                {{ inclusion.type === 'supplier' ? `Supplier(${inclusion.serviceType || inclusion.data?.service || 'General'})` : inclusion.type }}
              </td>
              <td class="border border-gray-300 px-4 py-2">{{ getInclusionName(inclusion) }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ getInclusionPrice(inclusion) }}</td>
              <td class="border border-gray-300 py-2">
                <div @click="removeInclusionFromEdit(index)" class="inline-block cursor-pointer">
                  <img 
                    alt="Delete Icon" 
                    class="w-[20px] h-[20px] transition-transform transform hover:scale-110 hover:brightness-90" 
                    src="/img/delete.png" 
                  >
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="mt-4 p-4 bg-gray-50 rounded-lg shadow-sm">
          <div class="flex justify-between items-center">
            <div class="text-lg font-semibold text-gray-700">Total Package Price:</div>
            <div class="text-xl font-bold text-blue-600">{{ formatPrice(
              selectedPackage.inclusions.reduce((total, inc) => {
                if (inc.type === 'supplier' && inc.data) total += Number(inc.data.price || 0);
                if (inc.type === 'venue' && inc.data) total += Number(inc.data.venue_price || 0);
                if (inc.type === 'outfit' && inc.data) total += Number(inc.data.gown_package_price || 0);
                if (inc.type === 'service' && inc.data) total += Number(inc.data.add_service_price || 0);
                return total;
              }, 0)
            ) }}</div>
          </div>
          <div class="mt-2 text-sm text-gray-500">
            * Price includes all selected inclusions (suppliers, services, venue, and outfit package)
          </div>
        </div>
      </div>

      <!-- Submit and Delete Buttons -->
      <div class="flex justify-center space-x-4 mt-8">
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Update Package</button>
        
      </div>
    </div>
  </form>


    
    
    </div>
    </template>

    <script>
import axios from 'axios';

axios.defaults.withCredentials = true;

export default {
  name: 'AddServices',
  data() {
    return {
      showAddEventTypeModal: false,
      newEventTypeName: "",
      showTable: 'packages',
      currentPackagesPage: 1,
      rowsPerPackagesPage: 5,
      errorMessage: '',
      addPackagesForm: false,
      editPackagesForm: false,
      addPackagesDetails: false,
      addStaffDetails: false,
      inclusionType: '',
      selectedInclusion: '',
      selectedSupplierType: '',
      selectedSupplier: null,
      selectedVenue: null,
      selectedOutfit: null,
      selectedService: null,
      showInclusionModal: false,
      showSupplierModal: false,
      showVenueModal: false,
      showOutfitModal: false,
      showServiceModal: false,
      inclusions: [],
      selectedInclusionType: '',
      supplierTypes: [
        'Catering',
        'Photographer',
        'Videographer',
        'Entertainment',
        'Sound and Lighting',
        'Transportation',
        'Host',
        'Invitations',
        'Keepsakes',
        'Hair Stylist',
        'Makeup Artist',
      ],
      eventTypes: [],
      availableSuppliers: [],
      venues: [], 
      gownPackages: [],
      additionalServices: [],
      packageData: {
        package_name: '',
        event_type_id: '',
        venue_id: null,
        capacity: null,
        additional_capacity_charges: null,
        charge_unit: 1,
        description: '',
        suppliers: [],
        additional_services: [],
      },
      packages: [],
      selectedPackage: {
        packageId: null,
        package_name: '',
        event_type_id: '',
        capacity: 0,
        total_price: 0,
        description: '',
        inclusions: [],
        selectedSuppliers: [],
        selectedVenue: null,
        selectedOutfitPackage: null,
        selectedAdditionalServices: []
      },
      
    };
  },
 
  methods: {
    addNewEventType() {
      this.showAddEventTypeModal = true; // Show modal
      this.packageData.event_type_id = ""; // Reset selection
    },
    closeAddEventTypeModal() {
      this.showAddEventTypeModal = false; // Hide modal
      this.newEventTypeName = ""; // Reset input
    },
    
    async saveNewEventType() {
        if (!this.newEventTypeName.trim()) {
          alert("Event type name cannot be empty.");
          return;
        }

        try {
          const response = await axios.post('http://127.0.0.1:5000/create-event-type', 
            { event_type_name: this.newEventTypeName.trim() },
            {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              },
            }
          );

          const newEventType = response.data.event_type;
          this.eventTypes.push(newEventType);
          this.packageData.event_type_id = newEventType.event_type_id;
          this.closeAddEventTypeModal();
          alert('Event type added successfully!');
        } catch (error) {
          console.error('Error creating event type:', error);
          alert(error.response?.data?.error || 'Failed to create event type');
        }
      },
    openInclusionModal(type) {
        this.selectedInclusionType = type;  // Add this line
        switch (type) {
          case 'supplier':
            this.showInclusionModal = true;
            break;
          case 'venue':
            this.openVenueModal();
            break;
          case 'outfit':
            this.openOutfitModal();
            break;
          case 'service':
            this.openServiceModal();
            break;
        }
      },
    closeInclusionModal() {
      this.showInclusionModal = false;
    },
    openSupplierModal() {
      this.showSupplierModal = true;
    },
    closeSupplierModal() {
      this.showSupplierModal = false;
    },
    openVenueModal() {
      console.log('Opening venue modal');
      console.log('Current venues:', this.venues);
      this.showVenueModal = true;
    },
    closeVenueModal() {
      this.showVenueModal = false;
    },
    openOutfitModal() {
      this.showOutfitModal = true;
    },
    closeOutfitModal() {
      this.showOutfitModal = false;
    },
    openServiceModal() {
      this.showServiceModal = true;
    },
    closeServiceModal() {
      this.showServiceModal = false;
    },
    selectSupplierType(serviceType) {
      this.selectedSupplierType = serviceType;
      this.closeInclusionModal();
      this.openSupplierModal();
    },
    addSelectedSupplier() {
      if (this.selectedSupplier && this.selectedSupplierType) {
        const newInclusion = {
          type: 'supplier',
          serviceType: this.selectedSupplierType,
          data: {
            ...this.selectedSupplier,
            service: this.selectedSupplierType
          }
        };
        
        // Add to the active inclusions list based on which modal is active
        if (this.editPackagesForm && this.selectedPackage) {
          this.selectedPackage.inclusions.push(newInclusion);
        } else {
          this.inclusions.push(newInclusion);
        }
        
        this.selectedSupplier = null;
        this.closeSupplierModal();
      }
    },
    addSelectedVenue() {
      if (this.selectedVenue) {
        const newInclusion = {
          type: 'venue',
          data: this.selectedVenue
        };
        
        // Add to the active inclusions list based on which modal is active
        if (this.editPackagesForm && this.selectedPackage) {
          // Remove any existing venue first (only one venue allowed)
          this.selectedPackage.inclusions = this.selectedPackage.inclusions.filter(inc => inc.type !== 'venue');
          this.selectedPackage.inclusions.push(newInclusion);
        } else {
          // Remove any existing venue first (only one venue allowed)
          this.inclusions = this.inclusions.filter(inc => inc.type !== 'venue');
          this.inclusions.push(newInclusion);
        }
        
        this.selectedVenue = null;
        this.closeVenueModal();
      }
    },
    addSelectedOutfit() {
      if (this.selectedOutfit) {
        const newInclusion = {
          type: 'outfit',
          data: this.selectedOutfit
        };
        
        // Add to the active inclusions list based on which modal is active
        if (this.editPackagesForm && this.selectedPackage) {
          // Remove any existing outfit first (only one outfit package allowed)
          this.selectedPackage.inclusions = this.selectedPackage.inclusions.filter(inc => inc.type !== 'outfit');
          this.selectedPackage.inclusions.push(newInclusion);
        } else {
          // Remove any existing outfit first (only one outfit package allowed)
          this.inclusions = this.inclusions.filter(inc => inc.type !== 'outfit');
          this.inclusions.push(newInclusion);
        }
        
        this.selectedOutfit = null;
        this.closeOutfitModal();
      }
    },
    addSelectedService() {
      if (!this.selectedService) {
        console.error('No service selected');
        return;
      }

      console.log('Adding service:', this.selectedService);
      
      const newInclusion = {
        type: 'service',
        data: {
          add_service_id: this.selectedService.add_service_id,
          add_service_name: this.selectedService.add_service_name,
          add_service_description: this.selectedService.add_service_description,
          add_service_price: this.selectedService.add_service_price,
          status: this.selectedService.status
        }
      };
      
      // Add to the active inclusions list based on which modal is active
      if (this.editPackagesForm && this.selectedPackage) {
        this.selectedPackage.inclusions.push(newInclusion);
      } else {
        this.inclusions.push(newInclusion);
      }

      this.selectedService = null;
      this.closeServiceModal();
    },
    getEventTypeName(eventTypeId) {
      const eventType = this.eventTypes.find(type => type.event_type_id === eventTypeId);
      return eventType ? eventType.event_type_name : 'N/A';
    },
    removeInclusion(index) {
      this.inclusions.splice(index, 1);
    },
    removeInclusionFromEdit(index) {
      if (this.selectedPackage && this.selectedPackage.inclusions) {
        this.selectedPackage.inclusions.splice(index, 1);
      }
    },
    filteredSuppliers(serviceType) {
      return this.availableSuppliers.filter(supplier => supplier.service === serviceType && !this.inclusions.find(inclusion => inclusion.type === 'supplier' && inclusion.data && inclusion.data.supplier_id === supplier.supplier_id));
    },
    getInclusionName(inclusion) {
      // Get the name of an inclusion based on its type
      if (!inclusion || !inclusion.data) return 'Unknown';
      
      switch (inclusion.type) {
        case 'supplier':
          const firstName = inclusion.data.firstname || '';
          const lastName = inclusion.data.lastname || '';
          
          if (firstName || lastName) {
            return `${firstName} ${lastName}`.trim();
          } else if (inclusion.data.name) {
            return inclusion.data.name;
          } else {
            return 'Unnamed Supplier';
          }
          
        case 'venue':
          return inclusion.data.venue_name || 'Unnamed Venue';
          
        case 'outfit':
          return inclusion.data.gown_package_name || 'Unnamed Outfit Package';
          
        case 'service':
          return inclusion.data.add_service_name || inclusion.data.name || 'Unnamed Service';
          
        default:
          return 'Unknown';
      }
    },
    getInclusionPrice(inclusion) {
      // Get the formatted price of an inclusion based on its type
      if (!inclusion || !inclusion.data) return this.formatPrice(0);
      
      try {
        const priceMap = {
          supplier: 'price',
          venue: 'venue_price', 
          outfit: 'gown_package_price',
          service: 'add_service_price'
        };
        
        const priceField = priceMap[inclusion.type];
        if (!priceField) return this.formatPrice(0);
        
        let price = 0;
        
        // Try to get price from the data object
        if (inclusion.data[priceField] !== undefined) {
          price = parseFloat(inclusion.data[priceField]) || 0;
        } 
        // Alternative price fields based on API response format
        else if (inclusion.type === 'service' && inclusion.data.price !== undefined) {
          price = parseFloat(inclusion.data.price) || 0;
        }
        
        return `${this.formatPrice(price)} php`;
      } catch (error) {
        console.error(`Error getting price for inclusion:`, inclusion, error);
        return this.formatPrice(0) + ' php';
      }
    },

      async addPackages() {
          try {
            // Validate that all inclusions have data selected
            const hasEmptyInclusions = this.inclusions.some(inclusion => !inclusion.data);
            if (hasEmptyInclusions) {
              alert('Please select all inclusion details before submitting.');
              return;
            }

            // Prepare package data with explicit conversion and validation
            const packageData = {
              package_name: this.packageData.package_name,
              event_type_id: this.packageData.event_type_id,
              venue_id: this.inclusions.find(inc => inc.type === 'venue' && inc.data)?.data?.venue_id || null,
              capacity: Number(this.packageData.capacity),
              additional_capacity_charges: Number(this.packageData.additional_capacity_charges),
              charge_unit: Number(this.packageData.charge_unit),
              description: this.packageData.description,
              suppliers: this.inclusions
              .filter(inclusion => inclusion.type === 'supplier' && inclusion.data)
              .map(inclusion => ({
                supplier_id: Number(inclusion.data.supplier_id),
                type: 'internal',  // All suppliers are internal
                price: Number(inclusion.data.price || 0),
                remarks: `${inclusion.serviceType} service`
              })),
              gown_package_id: this.inclusions.find(inc => inc.type === 'outfit' && inc.data)?.data?.gown_package_id || null,
              additional_services: this.inclusions
                .filter(inclusion => inclusion.type === 'service' && inclusion.data)
                .map(inclusion => ({
                  add_service_id: Number(inclusion.data.add_service_id),
                  add_service_price: Number(inclusion.data.add_service_price),
                })),
              total_price: 0, // Initialize total price
            };

           // Calculate total price
            packageData.total_price = 
              // Supplier prices
              packageData.suppliers.reduce((acc, supplier) => acc + (supplier.price || 0), 0) +
              // Additional service prices
              packageData.additional_services.reduce((acc, service) => acc + (service.add_service_price || 0), 0) +
              // Venue price
              Number(this.inclusions.find(inc => inc.type === 'venue' && inc.data)?.data?.venue_price || 0) +
              // Outfit package price
              Number(this.inclusions.find(inc => inc.type === 'outfit' && inc.data)?.data?.gown_package_price || 0);
                
              // Add this for debugging
              console.log('Price breakdown:', {
                suppliers: packageData.suppliers.reduce((acc, supplier) => acc + (supplier.price || 0), 0),
                additionalServices: packageData.additional_services.reduce((acc, service) => acc + (service.add_service_price || 0), 0),
                venue: Number(this.inclusions.find(inc => inc.type === 'venue' && inc.data)?.data?.venue_price || 0),
                outfit: Number(this.inclusions.find(inc => inc.type === 'outfit' && inc.data)?.data?.gown_package_price || 0),
                total: packageData.total_price
              });

              if (!packageData.package_name || !packageData.event_type_id) {
                  alert('Package name and event type are required.');
                  return;
                }

            if (packageData.suppliers.length === 0) {
              alert('At least one supplier is required.');
              return;
            }

            console.log('Sending package data:', packageData);  // Debug log

            const response = await axios.post('http://127.0.0.1:5000/create-package', packageData, {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              },
            });

            if (response.status === 201) {
              alert('Package created successfully!');
              this.resetPackageForm();
              this.fetchPackages(); // Refresh the packages list
            }
          } catch (error) {
            console.error('Error creating package:', error);
            let errorMessage = 'Failed to create package. Please try again.';
            
            if (error.response) {
              console.error('Error response:', error.response.data);
              errorMessage = error.response.data.message || 
                            error.response.data.error || 
                            'Failed to create package. Please check your input.';
            }
            
            alert(errorMessage);
            this.errorMessage = errorMessage;
          }
        },


    resetPackageForm() {
      this.packageData = {
        package_name: '',
        event_type_id: '',
        venue_id: null,
        capacity: null,
        additional_capacity_charges: null,
        charge_unit: 1,
        description: '',
        suppliers: [],
        additional_services: [],
      };
      this.inclusions = [];
      this.addPackagesForm = false;
    },
    closePackagesForm() {
      this.resetPackageForm();
    },

    addVenue() {
    if (this.selectedVenue) {
      this.inclusions.push({
        type: 'venue',
        data: this.selectedVenue
      });
      this.selectedVenue = null;
    }
  },
  addOutfit() {
    if (this.selectedOutfit) {
      this.inclusions.push({
        type: 'outfit',
        data: this.selectedOutfit
      });
      this.selectedOutfit = null;
    }
  },




  async fetchPackages() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('You are not logged in. Please log in to view packages.');
          return;
        }

        // First fetch event types to ensure we have the mapping
        await this.fetchEventTypes();

        const response = await axios.get('http://127.0.0.1:5000/created-packages', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          withCredentials: true,
        });

        console.log("Raw package data from API:", response.data);

        this.packages = response.data.map((pkg, index) => {
          // Ensure all data fields have default values to prevent undefined or NaN issues
          const venue_price = parseFloat(pkg.venue_price) || 0;
          
          // Process suppliers - ensure service_type is available
          const suppliers = (pkg.suppliers || []).map(supplier => {
            return {
              ...supplier,
              supplier_id: supplier.supplier_id,
              firstname: supplier.name ? supplier.name.split(' ')[0] : '',
              lastname: supplier.name ? supplier.name.split(' ')[1] || '' : '',
              service_type: supplier.service || 'General',
              price: parseFloat(supplier.price) || 0,
              status: supplier.status || 'Active'
            };
          });
          
          // Process additional services
          const additionalServices = (pkg.additional_services || []).map(service => {
            return {
              add_service_id: service.service_id,
              add_service_name: service.name || '',
              add_service_description: service.description || '',
              add_service_price: parseFloat(service.price) || 0,
              status: service.status || 'Active'
            };
          });

          // Create properly formatted inclusions from various data sources
          const inclusions = [
            ...suppliers.map(supplier => ({
              type: 'supplier',
              serviceType: supplier.service_type,
              data: supplier
            })),
            ...(pkg.venue_id ? [{
              type: 'venue',
              data: { 
                venue_id: pkg.venue_id, 
                venue_name: pkg.venue_name || 'Unknown Venue',
                venue_price: venue_price,
                location: pkg.location || 'No location specified'
              }
            }] : []),
            ...(pkg.gown_package_id ? [{
              type: 'outfit',
              data: { 
                gown_package_id: pkg.gown_package_id,
                gown_package_name: pkg.gown_package_name || 'Unknown Outfit',
                gown_package_price: parseFloat(pkg.gown_package_price) || 0
              }
            }] : []),
            ...additionalServices.map(service => ({
              type: 'service',
              data: service
            }))
          ];

          // Get the proper event type name from our eventTypes list
          const eventType = this.eventTypes.find(t => t.event_type_id === pkg.event_type_id);
          const eventTypeName = eventType ? eventType.event_type_name : pkg.event_type_name || 'Unknown Type';

          console.log(`Processed package ${pkg.package_id}:`, { 
            suppliers, 
            additionalServices, 
            venue: pkg.venue_id ? { 
              venue_id: pkg.venue_id, 
              venue_name: pkg.venue_name,
              venue_price: venue_price 
            } : null,
            inclusions,
            eventTypeName
          });

          return {
            packageId: pkg.package_id,
            package_name: pkg.package_name,
            event_type_id: pkg.event_type_id,
            event_type_name: eventTypeName,
            package_type: eventTypeName,
            capacity: pkg.capacity || 0,
            total_price: parseFloat(pkg.total_price) || 0,
            description: pkg.description || '',
            venue_id: pkg.venue_id,
            venue_name: pkg.venue_name || '',
            venue_price: venue_price,
            location: pkg.location || '',
            gown_package_id: pkg.gown_package_id,
            gown_package_name: pkg.gown_package_name || '',
            suppliers,
            additional_services: additionalServices,
            inclusions,
            dummyIndex: index + 1
          };
        });
        
        console.log("Processed packages data:", this.packages);
      } catch (error) {
        console.error('Error fetching packages:', error.response?.data || error.message);
      }
    },
    async fetchVenues() {
      try {
        console.log('Fetching venues from database...');
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error('No access token found');
          return;
        }

        // Try the correct API endpoints sequentially until one works
        let response = null;
        let endpoints = [
          '/venues',               // Main endpoint
          '/created-venues',       // Alternate endpoint
          '/available-venues',     // Another possible endpoint 
          '/api/venues'            // API-prefixed endpoint
        ];
        
        let venuesData = [];
        
        // Try each endpoint until we get data
        for (const endpoint of endpoints) {
          try {
            console.log(`Trying endpoint: http://127.0.0.1:5000${endpoint}`);
            response = await axios.get(`http://127.0.0.1:5000${endpoint}`, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            
            console.log(`Response from ${endpoint}:`, response.data);
            
            // Process response based on format
            if (Array.isArray(response.data)) {
              venuesData = response.data;
            } else if (response.data && typeof response.data === 'object') {
              if (response.data.data && Array.isArray(response.data.data)) {
                venuesData = response.data.data;
              } else if (response.data.venues && Array.isArray(response.data.venues)) {
                venuesData = response.data.venues;
              }
            }
            
            // If we got data, stop trying endpoints
            if (venuesData.length > 0) {
              console.log(`Found venues data from ${endpoint}:`, venuesData);
              break;
            }
          } catch (endpointError) {
            console.log(`Error with endpoint ${endpoint}:`, endpointError.message);
          }
        }
        
        // If we found any venues data, format it for the component
        if (venuesData.length > 0) {
          this.venues = venuesData
            .filter(venue => venue.status === 'Active' || venue.status === undefined)
            .map(venue => ({
              venue_id: venue.venue_id,
              venue_name: venue.venue_name,
              location: venue.location || 'No location specified',
              venue_price: parseFloat(venue.venue_price) || 0,
              description: venue.description || '',
              capacity: venue.venue_capacity || venue.capacity || 0,
              status: venue.status || 'Active',
              image: venue.image
            }));
          console.log('Processed venues for component:', this.venues);
        } else {
          // No venues found from any endpoint
          console.error('Failed to fetch venues from all endpoints, or all responses were empty.');
          this.venues = [];
        }
      } catch (error) {
        console.error('Error in fetchVenues:', error);
        if (error.response) {
          console.error('Error response data:', error.response.data);
        }
        this.venues = [];
      }
    },


      async fetchSuppliersAndPackageServices() {
            try {
              const token = localStorage.getItem('access_token');
              if (!token) {
                console.error('No access token found');
                return;
              }

              const [suppliersResponse, gownPackagesResponse] = await Promise.all([
                axios.get('http://127.0.0.1:5000/suppliers', {
                  headers: { Authorization: `Bearer ${token}` },
                }),
                axios.get('http://127.0.0.1:5000/gown-packages', {
                  headers: { Authorization: `Bearer ${token}` },
                }),
              ]);


              this.availableSuppliers = suppliersResponse.data.filter(supplier => supplier.status === 'Active');
              this.gownPackages = gownPackagesResponse.data
                .filter(gp => gp.status === 'Active')
                .map(gp => ({
                  ...gp,
                  gown_package_id: gp.gown_package_id,
                  gown_package_name: gp.gown_package_name,
                  gown_package_price: gp.gown_package_price,
                }));

              
            } catch (error) {
              console.error('Error fetching data:', error);
              console.error('Error details:', error.response?.data || error.message);
            }
        },

        async fetchEventTypes() {
          try {
              const response = await axios.get('http://127.0.0.1:5000/event-types');
              this.eventTypes = response.data;
          } catch (error) {
              console.error('Error fetching event types:', error);
              console.error('Error details:', error.response ? error.response.data : error.message);
          }
      },

    addSupplier() {
        this.packageData.suppliers.push({
        type: 'internal',
        supplier_id: '',
        external_supplier_name: '',
        external_supplier_contact: '',
        external_supplier_price: null,
        remarks: ''
      });
    },
    resetSupplierFields(supplier) {
      if (supplier.type === 'internal') {
        supplier.external_supplier_name = '';
        supplier.external_supplier_contact = '';
        supplier.external_supplier_price = null;
      } else {
        supplier.supplier_id = '';
      }
      supplier.remarks = '';
    },
    removeSupplier(index) {
      this.packageData.suppliers.splice(index, 1);
    },
    async fetchAdditionalServices() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) return;

          const response = await axios.get('http://127.0.0.1:5000/additional-services', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          let servicesData = [];
          if (response.data && typeof response.data === 'object') {
            if (Array.isArray(response.data)) {
              servicesData = response.data;
            } else if (response.data.data && Array.isArray(response.data.data)) {
              servicesData = response.data.data;
            }
          }

          this.additionalServices = servicesData.map(service => ({
            add_service_id: service.add_service_id,
            add_service_name: service.add_service_name,
            add_service_description: service.add_service_description || 'No description available',
            add_service_price: parseFloat(service.add_service_price) || 0,
            status: service.status || 'Active'
          }));
        
        } catch (error) {
          if (error.response) {
            console.error('Error response:', error.response.data);
          }
        }
    },


      async confirmEditPackage() {
          try {
            const token = localStorage.getItem('access_token');

            if (!this.selectedPackage || !this.selectedPackage.packageId) {
                alert("Package ID is missing or invalid.");
                return;
            }

            // Calculate total price from inclusions
            const totalPrice = this.dynamicTotalPrice;

            // Prepare update data
            const updateData = {
                package_name: this.selectedPackage.package_name,
                event_type_id: this.selectedPackage.event_type_id,
                package_type: this.getEventTypeName(this.selectedPackage.event_type_id),
                capacity: this.selectedPackage.capacity,
                price: totalPrice,
                description: this.selectedPackage.description,
                inclusions: this.prepareInclusionsForAPI(this.selectedPackage.inclusions)
            };

            console.log("Sending update data:", updateData);

            const response = await axios.put(
                `http://127.0.0.1:5000/created-package/${this.selectedPackage.packageId}`,
                updateData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.status === 200) {
                alert('Package updated successfully!');
                await this.fetchPackages(); // Refresh the packages list
                this.closeEditPackagesBtn();
            }
          } catch (error) {
            console.error('Error updating package:', error);
            if (error.response) {
                alert(`Error updating package: ${error.response.data.message || error.response.data.error || 'Unknown error'}`);
            } else {
                alert('Error updating package. Please try again.');
            }
          }
      },

    prepareInclusionsForAPI(inclusions) {
        // Format inclusions for the API
        return inclusions.map(inclusion => {
            const type = inclusion.type;
            const data = inclusion.data || {};
            
            if (type === 'supplier') {
                return {
                    type: 'supplier',
                    id: data.supplier_id,
                    price: parseFloat(data.price || 0),
                    serviceType: inclusion.serviceType || data.service
                };
            } else if (type === 'venue') {
                return {
                    type: 'venue',
                    id: data.venue_id,
                    price: parseFloat(data.venue_price || 0)
                };
            } else if (type === 'outfit') {
                return {
                    type: 'outfit',
                    id: data.gown_package_id,
                    price: parseFloat(data.gown_package_price || 0)
                };
            } else if (type === 'service') {
                return {
                    type: 'service',
                    id: data.add_service_id,
                    price: parseFloat(data.add_service_price || 0)
                };
            }
            return null;
        }).filter(item => item !== null);
    },

    async deletePackage(packageId) {
        try {
            if (!confirm('Are you sure you want to delete this package? This action cannot be undone.')) {
                return;
            }

            const token = localStorage.getItem('access_token');
            if (!token) {
                alert('You are not logged in. Please log in to delete packages.');
                return;
            }

            const response = await axios.delete(`http://127.0.0.1:5000/created-package/${packageId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.status === 200) {
                alert('Package deleted successfully!');
                // Remove the deleted package from the packages array
                this.packages = this.packages.filter(packageItem => packageItem.packageId !== packageId);
                this.closeEditPackagesBtn();                      
            } else {
                alert('Failed to delete package.');
            }
        } catch (error) {
            console.error('Error deleting package:', error);
            if (error.response) {
                alert(`Error deleting package: ${error.response.data.message}`);
            } else {
                alert('Error deleting package. Please try again.');
            }
        }
    },

    changePackagesPage(page) {
        this.currentPackagesPage = page;
    },
    prevPackagesPage() {
        if (this.currentPackagesPage > 1) {
            this.currentPackagesPage--;
        }
    },
    nextPackagesPage() {
        if (this.currentPackagesPage < this.totalPackagesPages) {
            this.currentPackagesPage++;
        }
    },

    prevStaffsPage() {
      if (this.currentStaffsPage > 1) {
        this.currentStaffsPage--;
      }
    },
    nextStaffsPage() {
      if (this.currentStaffsPage < this.totalStaffsPages) {
        this.currentStaffsPage++;
      }
    },
    changeStaffsPage(page) {
      this.currentStaffsPage = page;
    },

    addPackagesBtn() {
      this.addPackagesForm = true;
    },
    closePackagesForm() {
      this.addPackagesForm = false;
    },


    editVendorBtn(){
      this.editVendorForm = true;
    },

    closeEditVendorBtn() {
      this.editVendorForm = false;
    },

    editPackageBtn(index) {
        console.log("Selected Package Index:", index);
        const packageToEdit = this.paginatedPackages[index];
        console.log("Original Package Data:", JSON.parse(JSON.stringify(packageToEdit)));
        
        // Get the proper event type name for the package
        const eventType = this.eventTypes.find(t => t.event_type_id === packageToEdit.event_type_id);
        const eventTypeName = eventType ? eventType.event_type_name : packageToEdit.event_type_name || 'Unknown Type';
        
        // Initialize the selected package with complete data
        this.selectedPackage = {
            packageId: packageToEdit.packageId,
            package_name: packageToEdit.package_name,
            package_type: eventTypeName,
            event_type_id: packageToEdit.event_type_id,
            capacity: packageToEdit.capacity || 0,
            total_price: packageToEdit.total_price || 0,
            description: packageToEdit.description || '',
            inclusions: [],
            venue_id: packageToEdit.venue_id,
            venue_name: packageToEdit.venue_name,
            venue_price: packageToEdit.venue_price
        };

        // Copy inclusions from the original package to the selected package
        if (packageToEdit.inclusions && packageToEdit.inclusions.length > 0) {
            // Make a deep copy of the inclusions and ensure all properties are valid
            this.selectedPackage.inclusions = JSON.parse(JSON.stringify(packageToEdit.inclusions)).map(inclusion => {
                // Ensure data property exists
                if (!inclusion.data) {
                    inclusion.data = {};
                }
                
                // Fix supplier-specific data
                if (inclusion.type === 'supplier') {
                    if (!inclusion.serviceType && inclusion.data.service) {
                        inclusion.serviceType = inclusion.data.service;
                    }
                    // Ensure price is a valid number
                    if (inclusion.data.price) {
                        inclusion.data.price = parseFloat(inclusion.data.price);
                    }
                }
                
                // Fix venue-specific data
                if (inclusion.type === 'venue' && inclusion.data) {
                    // Ensure venue_price is a valid number
                    if (inclusion.data.venue_price) {
                        inclusion.data.venue_price = parseFloat(inclusion.data.venue_price);
                    } else if (packageToEdit.venue_price) {
                        inclusion.data.venue_price = parseFloat(packageToEdit.venue_price);
                    } else {
                        // Query the venues list to get the price if it's not in the inclusion data
                        const venueFromList = this.venues.find(v => v.venue_id === inclusion.data.venue_id);
                        if (venueFromList) {
                            inclusion.data.venue_price = parseFloat(venueFromList.venue_price) || 0;
                        }
                    }
                }
                
                // Fix outfit-specific data
                if (inclusion.type === 'outfit' && inclusion.data) {
                    // Ensure gown_package_price is a valid number
                    if (inclusion.data.gown_package_price) {
                        inclusion.data.gown_package_price = parseFloat(inclusion.data.gown_package_price);
                    }
                }
                
                // Fix service-specific data
                if (inclusion.type === 'service' && inclusion.data) {
                    // Ensure add_service_price is a valid number
                    if (inclusion.data.add_service_price) {
                        inclusion.data.add_service_price = parseFloat(inclusion.data.add_service_price);
                    }
                }
                
                return inclusion;
            });
            console.log("Processed inclusions for editing:", this.selectedPackage.inclusions);
        }

        // Set inclusions as a reference for the package edit form
        this.inclusions = this.selectedPackage.inclusions;
        
        console.log("Prepared Package for Editing:", this.selectedPackage);
        this.editPackagesForm = true;
    },
        closeEditPackagesBtn() {
        this.editPackagesForm = false;
        this.selectedPackage = null;
        // Reset inclusions when closing the edit form 
        this.inclusions = [];
    },

    nextPackageForm() {
        this.packageDetails = false;
    },

    formatPrice(price) {
      return new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP'
      }).format(price);
    },

    displayEventTypeBtn() {
      this.showAddEventTypeModal = true;
      this.newEventTypeName = '';  // Reset the input field
    },
    
        
    
    
  },
  computed: {
    totalPackagesPages() {
        return Math.ceil(this.packages.length / this.rowsPerPackagesPage);
    },
    paginatedPackages() {
        if (!this.packages || this.packages.length === 0) {
            return []; // Ensure it's an empty array if packages is not available
        }
        const start = (this.currentPackagesPage - 1) * this.rowsPerPackagesPage;
        const end = start + this.rowsPerPackagesPage;
        return this.packages.slice(start, end);
    },
    totalPackages() {
        return this.packages.length;
    },
    startIndex() {
        return (this.currentPackagesPage - 1) * this.rowsPerPackagesPage + 1;
    },
    supplierPrice() {
    return this.supplier.price || this.supplier.external_supplier_price || 0;
   },
   filteredAdditionalServices() {
      if (!this.additionalServices || !Array.isArray(this.additionalServices)) {
        return [];
      }

      const selectedServiceIds = this.inclusions
        .filter(inc => inc.type === 'service' && inc.data)
        .map(inc => inc.data.add_service_id);

      return this.additionalServices.filter(service => 
        service.status === 'Active' && !selectedServiceIds.includes(service.add_service_id)
      );
    },
   filteredVenues() {
      return this.venues || [];
   },

  dynamicTotalPrice() {
      return (
        // Supplier prices
        this.inclusions
          .filter(inc => inc.type === 'supplier' && inc.data)
          .reduce((total, inc) => total + (Number(inc.data.price) || 0), 0) +
        // Additional service prices
        this.inclusions
          .filter(inc => inc.type === 'service' && inc.data)
          .reduce((total, inc) => total + (Number(inc.data.add_service_price) || 0), 0) +
        // Venue price
        Number(this.inclusions.find(inc => inc.type === 'venue' && inc.data)?.data?.venue_price || 0) +
        // Outfit package price
        Number(this.inclusions.find(inc => inc.type === 'outfit' && inc.data)?.data?.gown_package_price || 0)
      );
    }

  
},

    async mounted() {
      try {
        await this.fetchVenues();
        await this.fetchAdditionalServices();
        await this.fetchEventTypes();
        await this.fetchPackages();
        await this.fetchSuppliersAndPackageServices();
      } catch (error) {
        console.error('Error during data fetch in mounted hook:', error);
      }
    },


    watch: {
        showTable(newTable) {
            if (newTable === 'packages') {
                this.fetchPackages();
            } else if (newTable === 'vendors') {
                this.fetchVendors();
            }
        },
        packageData: {
          handler(newVal) {
            if (newVal.event_type_id === "add-new") {
              this.addNewEventType();
            }
          },
          deep: true,
        },
    },
};
    </script>

    <style scoped>
    </style>