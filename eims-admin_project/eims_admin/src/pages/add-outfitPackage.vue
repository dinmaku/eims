<template>
    <div class="bg-gray-200 w-full h-full overflow-y-auto">
        <!-- Alert Modal -->
        <div v-if="showAlert" class="fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto flex justify-center items-center z-50">
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
            
        <div class="w-full h-[65px] bg-gray-100 mt-2 flex items-center justify-between px-5 shadow-lg">
        <h1 class="font-inter font-extraLight text-3xl">
            Outfit Packages
        </h1>
        <button 
            class="bg-[#9B111E] text-white px-3 py-2 rounded shadow-lg transition-transform duration-300 transform hover:scale-105 font-semibold" 
            @click="showInactivePackagesModal"
        >
            Inactive Packages
        </button>
        </div>
    
        <div class="flex flex-row items-center m-5 space-x-5">
        <div class="flex justify-start w-52 h-20 bg-white rounded-lg shadow-lg px-2 items-center border-l-2 border-green-400 space-x-5">
            <h2 class="font-inter text-4xl font-bold mb-0"> {{ totalOutfitPackages }} <span class = "text-sm antialiased text-gray-600">packages</span></h2>
        </div>
        <button 
        @click="showOutfitsModalFn"
        class="flex items-center bg-white text-gray-800 font-inter mt-10 px-3 py-2 rounded shadow-lg transition-transform duration-300 transform hover:scale-105 font-semibold"
         > 

        View All Outfits
    </button>
    </div>
    
    <div class="flex flex-row justify-end items-center m-5 my-7">
        <button class = "mr-2 w-44 h-10 bg-[#9B111E] font-semibold text-gray-100 font-inter rounded-md shadow-lg 
        transition-transform duration-300 transform hover:scale-105" @click="addOutfitsPackageBtn">
        Create Package
        </button>
		<button class = "mr-2 w-44 h-10 bg-[#9B111E] font-semibold text-gray-100 font-inter rounded-md shadow-lg 
        transition-transform duration-300 transform hover:scale-105" @click="addOutfitsBtn">
        Add Outfit
        </button>
    </div>
    
            <!-- Gown Packages Table -->
                <div v-if="showTable === 'GownPackages'" class="relative shadow-md sm:rounded-xl w-full max-w-[1170px] h-[200] ml-5 mt-2 font-inter mb-10">
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 max-h-30 table-fixed">
                            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                <tr>
                                    <th scope="col" class="w-16 px-2 py-3">#</th>
                                    <th scope="col" class="w-52 px-2 py-3">Package Name</th>
                                    <th scope="col" class="w-96 px-2 py-3">Description</th>
                                    <th scope="col" class="w-36 px-2 py-3">Price</th>
                                    <th scope="col" class="w-28 px-2 py-3">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(gownPackage, index) in paginatedGownPackages"
                                    :key="gownPackage.gown_package_id"
                                    class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800">
                                    <th scope="row" class="w-16 px-2 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ gownPackage.dummyIndex }}</th>
                                    <td class="w-52 px-2 py-3 truncate">{{ gownPackage.gown_package_name }}</td>
                                    <td class="w-96 px-2 py-3 truncate">{{ gownPackage.description }}</td>
                                    <td class="w-36 px-2 py-3 truncate">{{ formatPrice(gownPackage.gown_package_price) }} php</td> 
                                    <td class="w-28 px-2 py-3">
                                    <div class="flex items-center space-x-2">
                                        <button
                                            class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
                                            @click="editGownPackageBtn(index)"
                                            title="Update">
                                            <img src="/img/update3.png" alt="Update" class="w-5 h-5">
                                        </button>
                                        <button
                                            class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
                                            @click="openStatusConfirmModal(gownPackage, (gownPackage.status || 'Active') === 'Active' ? 'Inactive' : 'Active')"
                                            :title="(gownPackage.status || 'Active') === 'Active' ? 'Set Inactive' : 'Set Active'">
                                            <img 
                                                :src="(gownPackage.status || 'Active') === 'Active' ? '/img/deactivate.png' : '/img/active2.png'" 
                                                :alt="(gownPackage.status || 'Active') === 'Active' ? 'Set Inactive' : 'Set Active'" 
                                                class="w-5 h-5">
                                        </button>
                                    </div>
                                </td>
                                                                                                            
                                </tr>
                            </tbody>
                        </table>

                        <!-- Pagination Controls -->
                        <div class="flex justify-center space-x-2 mt-4 mb-6">
                            <button @click="prevGownPackagePage" :disabled="currentGownPackagePage === 1"
                                class="px-3 py-1 bg-[#9B111E] text-white rounded-md hover:bg-[#B73A45] disabled:opacity-50 text-sm">Previous</button>
                            <button v-for="page in totalGownPackagePages" :key="page" @click="changeGownPackagePage(page)"
                                :class="{'bg-[#9B111E]': currentGownPackagePage === page, 'bg-gray-300': currentGownPackagePage !== page}"
                                class="px-3 py-1 text-white rounded-md hover:bg-[#B73A45] text-xs">
                                {{ page }}
                            </button>
                            <button @click="nextGownPackagePage" :disabled="currentGownPackagePage === totalGownPackagePages"
                                class="px-3 py-1 bg-[#9B111E] text-white rounded-md hover:bg-[#B73A45] disabled:opacity-50 text-xs">Next</button>
                        </div>
                    </div>
                </div>


        <div v-if="isInactivePackagesModalVisible" @click.self="closeInactivePackagesModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto flex justify-center items-center z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg w-[800px]">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold">Inactive Packages</h2>
                    <button @click="closeInactivePackagesModal" class="text-gray-500 hover:text-gray-700">
                        <span class="text-2xl">&times;</span>
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm text-left">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                            <tr>
                                <th class="px-4 py-3">Package Name</th>
                                <th class="px-4 py-3">Description</th>
                                <th class="px-4 py-3">Price</th>
                                <th class="px-4 py-3">Set</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="packages in inactivePackages" :key="packages.gown_package_id" class="border-b">
                                <td class="px-4 py-3">{{ packages.gown_package_name }}</td>
                                <td class="px-4 py-3">{{ packages.description }}</td>
                                <td class="px-4 py-3">{{ formatPrice(packages.gown_package_price) }} php</td>
                                <td class="px-4 py-3">
                                <button
                                    class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200"
                                    @click="openStatusConfirmModal(packages, 'Active')"
                                    title="Activate">
                                    <img src="/img/active2.png" alt="Set Active" class="w-5 h-5">
                                </button>
                            </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>


        <div v-if="showStatusConfirmModal" @click.self="closeStatusConfirmModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto flex justify-center items-center z-50">
            <div class="bg-white p-5 rounded-lg shadow-lg w-[400px]">
                <div class="flex flex-col items-center">
                    <h2 class="text-xl font-semibold mb-4">Confirm Status Change</h2>
                    <p class="mb-6 text-center">Are you sure you want to set this package to {{ pendingStatus }}?</p>
                    <div class="flex space-x-4">
                        <button
                            @click="closeStatusConfirmModal"
                            class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                        >
                            Cancel
                        </button>
                        <button
                            @click="confirmStatusChange"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-opacity-90"
                        >
                          Yes
                        </button>
                    </div>
                </div>
            </div>
        </div>

    
         
         <!-- Add Package Form -->    
        <form v-if="showOutfitPackageForm" @submit.prevent="submitPackage"
                @click.self="closePackageForm"
                class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center overflow-y-auto z-50"
            >
                <div class="bg-white w-full max-w-lg p-6 rounded-lg shadow-xl transform transition duration-300 relative">
                    <!-- Header -->
                    <div class="mb-6">
                        <h2 class="text-2xl font-bold text-gray-800 text-center">Add Outfit Package</h2>
                    </div>

                    <!-- Package Name -->
                    <div class="mb-4">
                        <label class="text-xs text-gray-600 block text-left">Package Name</label>
                        <input
                            type="text"
                            v-model="packageDetails.name"
                            class="mt-2 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                            required
                        />
                    </div>

               <!-- Description -->
                <div class="mb-4">
                        <label class="text-xs text-gray-600 block text-left">Description</label>
                    <textarea
                        v-model="packageDetails.description"
                        class="mt-2 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                        rows="3"
                        style="resize: none;"
                    ></textarea>
                </div>

                    <!-- Outfit Selection Buttons -->
                    <div class="flex justify-center space-x-4 my-6">
                        <button  @click="openOutfitSelection"
                            type="button"
                            class="px-4 py-2 bg-[#9B111E] text-white rounded-lg shadow-sm hover:bg-[#B73A45] transition duration-300"
                        >
                            Add Outfits
                        </button>
                    </div>

                    
            <!-- Inclusions Table -->
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">Inclusions</h3>
                <div class="border rounded-lg" style="height: 150px; overflow-y: auto;">
                    <table class="w-full">
                        <thead class="bg-gray-200 sticky top-0 z-10">
                            <tr>
                                <th class="p-2 text-left">Type</th>
                                <th class="p-2 text-left">Name</th>
                                <th class="p-2 text-left">Price</th>
                                <th class="p-2 text-left">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="outfit in packageInclusions"
                                :key="outfit.outfit_id"
                                class="hover:bg-gray-100 border-t"
                            >
                                <td class="p-2 text-sm capitalize">{{ outfit.outfit_type }}</td>
                                <td class="p-2 text-sm">{{ outfit.outfit_name }}</td>
                                <td class="p-2 text-sm">{{ formatPrice(outfit.rent_price) }} php</td>
                                <td class="p-2 text-sm">
                                    <button
                                        @click="removeOutfitFromPackage(outfit.outfit_id)"
                                    class="rounded p-1 hover:bg-red-100"
                                >
                                    <img 
                                        src="/img/delete.png"
                                        alt="Remove"
                                        class="w-4 h-4"
                                    />
                                </button>
                                </td>
                            </tr>
                        </tbody>
                </table>
            </div>
        </div>




            <!-- Price Summary Section -->
                <div class="mt-6 border-t pt-4">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Subtotal:</span>
                        <span class="font-semibold">₱ {{ formatPrice(calculateSubtotal()) }}</span>
                    </div>
                    
                    <!-- Discount Input -->
                    <div class="flex justify-between items-center mb-2">
                        <div class="flex items-center">
                            <span class="text-gray-600 mr-2">Discount (%):</span>
                            <input 
                                type="number" 
                                v-model.number="packageDetails.discount"
                                min="0"
                                max="100"
                                class="w-20 px-2 py-1 border rounded"
                            >
                        </div>
                        <span class="font-semibold ">- ₱ {{ formatPrice(calculateDiscount()) }}</span>
                    </div>

                    <!-- Total -->
                    <div class="flex justify-between items-center mt-4 pt-2 border-t">
                        <span class="text-lg font-bold">Total:</span>
                        <span class="text-lg font-bold ">₱ {{ formatPrice(calculateTotal()) }}</span>
                    </div>
                </div>

                    <!-- Actions -->
                    <div class="flex justify-end space-x-4 mt-6">
                        <button
                            @click="closePackageForm"
                            type="button"
                            class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg shadow-sm hover:bg-gray-400 transition duration-300"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-sm hover:bg-blue-700 transition duration-300"
                        >
                            Save
                        </button>
                    </div>
                </div>
            </form>

            <!-- Outfit Selection Modal -->
            <div v-if="showOutfitModal" @click.self="closeOutfitModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-[100]">
                <div class="bg-white w-full max-w-2xl p-6 rounded-lg shadow-xl">
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">Select Outfits</h3>
                    
                    <!-- Search Input -->
                    <div class="mb-4">
                        <input
                            type="text"
                            v-model="searchQuery"
                            placeholder="Search outfits..."
                            class="w-full px-4 py-2 border rounded-lg"
                        >
                    </div>

                    

                    <!-- Combined Outfits Table -->
                    <div style="max-height: 300px; overflow-y: auto;">
                    <table class="w-full text-sm">
                        <thead class="bg-gray-50 sticky top-0 z-10">
                            <tr>
                                <th scope="col" class="px-2 py-2 w-[30%]">Name</th>
                                <th scope="col" class="px-2 py-2 w-[30%]">Type</th>
                                <th scope="col" class="px-2 py-2 w-[25%]">Price</th>
                                <th scope="col" class="px-2 py-2 w-[15%]">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="outfit in filteredOutfits" :key="outfit.outfit_id" class="hover:bg-gray-50">
                            <td class="px-2 py-2 truncate">{{ outfit.outfit_name }}</td>
                            <td class="px-2 py-2 capitalize truncate">{{ outfit.outfit_type }}</td>
                            <td class="px-2 py-2">₱{{ formatPrice(outfit.rent_price) }}</td>
                            <td class="px-2 py-2 text-center">
                                <button
                                    @click="toggleOutfitSelection(outfit)"
                                    class="rounded p-1"
                                >
                                    <img 
                                        :src="isOutfitSelected(outfit.outfit_id) ? '/img/delete.png' : '/img/inlcude.png'" 
                                        :alt="isOutfitSelected(outfit.outfit_id) ? 'Remove' : 'Add'"
                                        class="w-6 h-6"
                                    />
                                </button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    </div>

                    <div class="mt-4 flex justify-end">
                        <button @click="closeOutfitModal" class="text-gray-600 hover:text-gray-800">
                            Close
                        </button>
                    </div>
                </div>
            </div>



            
           <!-- Edit Outfit Package Form -->
                <form v-if="editGownPackageForm" @click.self="closeEditGownPackageForm" @submit.prevent="updateGownPackage" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center overflow-y-auto z-50">
                <div class="bg-white w-full max-w-lg p-6 rounded-lg shadow-xl transform transition duration-300 relative">
                    <!-- Header -->
                    <div class="mb-6">
                        <h2 class="text-2xl font-bold text-gray-800 text-center">Update Outfit Package</h2>
                    </div>

                    <!-- Error Message -->
                    <div v-if="errorMessage" class="text-sm text-red-500 mb-4 text-center">
                    {{ errorMessage }}
                    </div>

                    <!-- Package Name -->
                    <div class="mb-4">
                        <label class="text-xs text-gray-600 block text-left">Package Name</label>
                    <input
                            id="package-name"
                        type="text"
                        v-model="selectedGownPackage.gown_package_name"
                            class="mt-2 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                        placeholder="Enter package name"
                        required
                    />
                    </div>

                    <!-- Description -->
                    <div class="mb-4">
                        <label class="text-xs text-gray-600 block text-left">Description</label>
                        <textarea
                        id="description"
                        v-model="selectedGownPackage.description"
                            class="mt-2 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
                        placeholder="Enter description"
                            rows="3"
                            style="resize: none;"
                        ></textarea>
                    </div>

                    <!-- Outfit Selection Button -->
                    <div class="flex justify-center space-x-4 my-6">
                        <button @click="openEditOutfitSelection"
                            type="button"
                            class="px-4 py-2 bg-[#9B111E] text-white rounded-lg shadow-sm hover:bg-[#B73A45] transition duration-300"
                        >
                            Add Outfits
                        </button>
                    </div>

                    <!-- Inclusions Section -->
                    <div class="mb-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-2">Inclusions</h3>
                        <div class="border rounded-lg" style="height: 150px; overflow-y: auto;">
                        <table class="w-full">
                                <thead class="bg-gray-200 sticky top-0 z-10">
                            <tr>
                                        <th class="p-2 text-left">Type</th>
                                        <th class="p-2 text-left">Name</th>
                                <th class="p-2 text-left">Price</th>
                                        <th class="p-2 text-left">Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                                    <!-- Combine both gowns and tuxedos -->
                            <tr 
                                        v-for="outfit in selectedPackageOutfits"
                                :key="outfit.outfit_id" 
                                        class="hover:bg-gray-100 border-t"
                                    >
                                        <td class="p-2 text-sm capitalize">{{ outfit.outfit_type }}</td>
                                <td class="p-2 text-sm">{{ outfit.outfit_name }}</td>
                                <td class="p-2 text-sm">{{ formatPrice(outfit.rent_price) }} php</td>
                                        <td class="p-2 text-sm">
                                            <button
                                                @click="removeOutfitFromPackage(outfit.outfit_id)"
                                                class="rounded p-1 hover:bg-red-100"
                                                type="button"
                                            >
                                                <img 
                                                    src="/img/delete.png"
                                                    alt="Remove"
                                                    class="w-4 h-4"
                                                />
                                            </button>
                                        </td>
                            </tr>
                            </tbody>
                        </table>
                        </div>
                    </div>

                

                    <!-- Price Summary Section -->
                    <div class="mt-6 border-t pt-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-gray-600">Subtotal:</span>
                            <span class="font-semibold">₱ {{ formatPrice(calculateEditSubtotal()) }}</span>
                        </div>
                        
                        <!-- Discount Input -->
                        <div class="flex justify-between items-center mb-2">
                            <div class="flex items-center">
                                <span class="text-gray-600 mr-2">Discount (%):</span>
                                    <input 
                                    type="number" 
                                    v-model.number="editDiscount"
                                    min="0"
                                    max="100"
                                    class="w-20 px-2 py-1 border rounded"
                                >
                            </div>
                            <span class="font-semibold ">- ₱ {{ formatPrice(calculateEditDiscount()) }}</span>
                        </div>

                        <!-- Total -->
                        <div class="flex justify-between items-center mt-4 pt-2 border-t">
                            <span class="text-lg font-bold">Total:</span>
                            <span class="text-lg font-bold ">₱ {{ formatPrice(calculateEditTotal()) }}</span>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex justify-end space-x-4 mt-6">
                    <button
                        @click="closeEditGownPackageForm"
                        type="button"
                            class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg shadow-sm hover:bg-gray-400 transition duration-300"
                    >
                            Cancel
                    </button>
                    <button
                        type="submit"
                            class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-sm hover:bg-blue-700 transition duration-300"
                    >
                            Update
                    </button>
                    </div>
                </div>
            </form>


            <!-- Add Outfit Form -->
            <form v-if="addOutfitForm" @submit.prevent="handleSubmit" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto" @click.self="closeAddOutfitForm">
                <div class="bg-white w-[1000px] p-5 rounded-lg shadow-lg overflow-y-auto">
                    <div class="flex justify-between items-center m-3">
                        <h1 class="font-semibold text-xl font-inter text-gray-800">Add Outfit</h1>
                    </div>
                    <div class="border border-gray-500 mt-5 items-center"></div>
                    <div class="m-5">
                        <span>{{ errorMessage }}</span>

                        <div class="flex flex-row gap-5">
                            <!-- Left Column - Input Fields -->
                            <div class="flex-1">
                                <!-- Outfit Name and Type -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Outfit Name</label>
                        <input type="text" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                            v-model="newOutfit.outfit_name" 
                            required>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Outfit Type</label>
                                        <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                        v-model="newOutfit.outfit_type" 
                                        required>
                                            <option value="" disabled selected>Select Type</option>
                                    <option value="Wedding Gown">Wedding Gown</option>
                                    <option value="Saree">Saree</option>
                                    <option value="Lehenga">Lehenga</option>
                                    <option value="Suit">Suit</option>
                                    <option value="Gown">Gown</option>
                                    <option value="Jumpsuit">Jumpsuit</option>
                                    <option value="Reception Dress">Reception Dress</option>
                                    <option value="Bridal Robe">Bridal Robe</option>
                                    <option value="Tuxedo">Tuxedo</option>
                                    <option value="Sherwani">Sherwani</option>
                                    <option value="Kurta Pajama">Kurta Pajama</option>
                                    <option value="Bespoke Tailored Outfit">Bespoke Tailored Outfit</option>
                                    <option value="Barong Tagalog">Barong Tagalog</option>
                                    <option value="Morning Coat">Morning Coat</option>
                                    <option value="Bridesmaid Dress">Bridesmaid Dress</option>
                                    <option value="Cultural Attire">Cultural Attire</option>
                                    <option value="Mix-and-Match Dress">Mix-and-Match Dress</option>
                                    <option value="Flower Girl Dress">Flower Girl Dress</option>
                                    <option value="Ring Bearer Suit">Ring Bearer Suit</option>
                                    <option value="Formal Attire">Formal Attire</option>
                                    <option value="Semi-Formal Attire">Semi-Formal Attire</option>
                                    <option value="Traditional/Tribal Wear">Traditional/Tribal Wear</option>
                                    <option value="Engagement Outfit">Engagement Outfit</option>
                                    <option value="Rehearsal Dinner Attire">Rehearsal Dinner Attire</option>
                                    <option value="Haldi Ceremony Outfit">Haldi Ceremony Outfit</option>
                                    <option value="Mehndi Ceremony Outfit">Mehndi Ceremony Outfit</option>
                                    <option value="Cocktail Party Wear">Cocktail Party Wear</option>
                                    <option value="Destination Wedding Attire">Destination Wedding Attire</option>
                                    <option value="Seasonal Attire">Seasonal Attire</option>
                                </select>
                                    </div>
                            </div>

                                <!-- Color and Price -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Outfit Color</label>
                                        <input type="text" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="newOutfit.outfit_color" 
                                            required>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Rent Price</label>
                                        <input type="number" 
                                            step="0.01" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="newOutfit.rent_price" 
                                            required>
                                    </div>
                        </div>

                                <!-- Size and Weight -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Size</label>
                                        <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="newOutfit.size" 
                                            required>
                                            <option value="" disabled selected>Select Size</option>
                                <option value="XS">XS</option>
                                <option value="S">S</option>
                                <option value="M">M</option>
                                <option value="L">L</option>
                                <option value="XL">XL</option>
                                <option value="2XL">2XL</option>
                                <option value="3XL">3XL</option>
                                <option value="4XL">4XL</option>
                                <option value="5XL">5XL</option>
                                </select>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block text-left">Weight (kg)</label>
                                        <input type="number" 
                                            step="0.01" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="newOutfit.weight" 
                                            required>
                                    </div>
                        </div>

                                <!-- Description -->
                        <div class="flex flex-col mt-5">
                                    <label class="text-xs text-gray-600 mb-2 block text-left">Outfit Description</label>
                                    <textarea class="p-2 w-full rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                        v-model="newOutfit.outfit_desc" placeholder="Description" rows="4" required></textarea>
                                </div>
                        </div>

                            <!-- Right Column - Image Upload -->
                            <div class="w-2/5">
                                <div class="flex flex-col">
                                    <label class="text-xs text-gray-600 mb-2">Outfit Image</label>
                                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <!-- Image Preview -->
                                        <div v-if="imagePreview" class="mb-4">
                                            <img :src="imagePreview" alt="Outfit Preview" class="max-w-full h-auto rounded-lg mx-auto mb-4">
                                        </div>
                                        <!-- Upload Button -->
                                        <label class="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600 inline-block">
                                            <span>{{ imagePreview ? 'Change Image' : 'Choose Image' }}</span>
                                    <input type="file" class="hidden" @change="onFileSelected" accept="image/*" ref="fileInput">
                                </label>
                                        <p class="mt-2 text-sm text-gray-500">{{ selectedFileName || 'No file chosen' }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Buttons -->
                        <div class="flex justify-end items-center mt-5 space-x-2">
                            <button class="w-20 h-10 bg-gray-300 text-white px-3 py-1 rounded transform transition duration-300 hover:scale-105 hover:bg-gray-400" @click="closeAddOutfitForm">
                                Cancel
                            </button>
                            <button type="submit" class="w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md transform transition duration-300 hover:scale-105">
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            </form>

            <!-- Edit Outfit Form -->
            <form v-if="isEditingOutfit" @submit.prevent="handleEditSubmit" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto z-50" @click.self="closeEditOutfitForm">
                <div class="bg-white w-[1000px] p-5 rounded-lg shadow-lg overflow-y-auto">
                    <div class="flex justify-between items-center m-3">
                        <h1 class="font-semibold text-xl font-inter text-gray-800">Edit Outfit</h1>
                    </div>
                    <div class="border border-gray-500 mt-5 items-center"></div>
                    <div class="m-5">
                        <span>{{ errorMessage }}</span>

                        <div class="flex flex-row gap-5">
                            <!-- Left Column - Input Fields -->
                            <div class="flex-1">
                                <!-- Outfit Name and Type -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Outfit Name</label>
                                        <input type="text" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.outfit_name" 
                                            required>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Outfit Type</label>
                                        <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.outfit_type" 
                                            required>
                                            <option value="" disabled selected>Select Type</option>
                                            <option value="Wedding Gown">Wedding Gown</option>
                                            <option value="Saree">Saree</option>
                                            <option value="Lehenga">Lehenga</option>
                                            <option value="Suit">Suit</option>
                                            <option value="Gown">Gown</option>
                                            <option value="Jumpsuit">Jumpsuit</option>
                                            <option value="Reception Dress">Reception Dress</option>
                                            <option value="Bridal Robe">Bridal Robe</option>
                                            <option value="Tuxedo">Tuxedo</option>
                                            <option value="Sherwani">Sherwani</option>
                                            <option value="Kurta Pajama">Kurta Pajama</option>
                                            <option value="Bespoke Tailored Outfit">Bespoke Tailored Outfit</option>
                                            <option value="Barong Tagalog">Barong Tagalog</option>
                                            <option value="Morning Coat">Morning Coat</option>
                                            <option value="Bridesmaid Dress">Bridesmaid Dress</option>
                                            <option value="Cultural Attire">Cultural Attire</option>
                                            <option value="Mix-and-Match Dress">Mix-and-Match Dress</option>
                                            <option value="Flower Girl Dress">Flower Girl Dress</option>
                                            <option value="Ring Bearer Suit">Ring Bearer Suit</option>
                                            <option value="Formal Attire">Formal Attire</option>
                                            <option value="Semi-Formal Attire">Semi-Formal Attire</option>
                                            <option value="Traditional/Tribal Wear">Traditional/Tribal Wear</option>
                                            <option value="Engagement Outfit">Engagement Outfit</option>
                                            <option value="Rehearsal Dinner Attire">Rehearsal Dinner Attire</option>
                                            <option value="Haldi Ceremony Outfit">Haldi Ceremony Outfit</option>
                                            <option value="Mehndi Ceremony Outfit">Mehndi Ceremony Outfit</option>
                                            <option value="Cocktail Party Wear">Cocktail Party Wear</option>
                                            <option value="Destination Wedding Attire">Destination Wedding Attire</option>
                                            <option value="Seasonal Attire">Seasonal Attire</option>
                                        </select>
                                    </div>
                                </div>

                                <!-- Color and Price -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Outfit Color</label>
                                        <input type="text" 
                                            class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.outfit_color" placeholder="Outfit Color" required>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Rent Price</label>
                                        <input type="number" step="0.01" class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.rent_price" placeholder="Rent Price" required>
                                    </div>
                                </div>

                                <!-- Size and Weight -->
                                <div class="flex flex-row mt-5 gap-2">
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Size</label>
                                        <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.size" required>
                                            <option value="" disabled selected>Select Size</option>
                                            <option value="XS">XS</option>
                                            <option value="S">S</option>
                                            <option value="M">M</option>
                                            <option value="L">L</option>
                                            <option value="XL">XL</option>
                                            <option value="2XL">2XL</option>
                                            <option value="3XL">3XL</option>
                                            <option value="4XL">4XL</option>
                                            <option value="5XL">5XL</option>
                                        </select>
                                    </div>
                                    <div class="w-full">
                                        <label class="text-xs text-gray-600 mb-2 block">Weight (kg)</label>
                                        <input type="number" step="0.01" class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                            v-model="editingOutfit.weight" placeholder="Weight" required>
                                    </div>
                                </div>

                                <!-- Status Toggle -->
                                <div class="flex flex-row mt-5 items-center">
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" 
                                               v-model="editingOutfit.status" 
                                               :true-value="'Available'" 
                                               :false-value="'Unavailable'" 
                                               class="sr-only peer">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer 
                                                  peer-checked:after:translate-x-full peer-checked:after:border-white 
                                                  after:content-[''] after:absolute after:top-[2px] after:left-[2px] 
                                                  after:bg-white after:border-gray-300 after:border after:rounded-full 
                                                  after:h-5 after:w-5 after:transition-all 
                                                  peer-checked:bg-green-600"></div>
                                        <span class="ml-3 text-sm font-medium text-gray-900">
                                            {{ editingOutfit.status }}
                                        </span>
                                    </label>
                                </div>

                                <!-- Description -->
                                <div class="flex flex-col mt-5">
                                    <label class="text-xs text-gray-600 mb-2">Outfit Description</label>
                                    <textarea class="p-2 w-full rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                        v-model="editingOutfit.outfit_desc" placeholder="Description" rows="4" required></textarea>
                                </div>
                            </div>

                            <!-- Right Column - Image Upload -->
                            <div class="w-2/5">
                                <div class="flex flex-col">
                                    <label class="text-xs text-gray-600 mb-2">Outfit Image</label>
                                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <!-- Image Preview -->
                                        <div v-if="editImagePreview" class="mb-4">
                                            <img :src="editImagePreview" alt="Outfit Preview" class="max-w-full h-auto rounded-lg mx-auto mb-4">
                                        </div>
                                        <!-- Upload Button -->
                                        <label class="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600 inline-block">
                                            <span>{{ editImagePreview ? 'Change Image' : 'Choose Image' }}</span>
                                            <input type="file" class="hidden" @change="onEditFileSelected" accept="image/*" ref="editFileInput">
                                        </label>
                                        <p class="mt-2 text-sm text-gray-500">{{ editingSelectedFileName || 'No file chosen' }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Buttons -->
                        <div class="flex justify-end items-center mt-5 space-x-2">
                            <button class="w-20 h-10 bg-gray-300 text-white px-3 py-1 rounded transform transition duration-300 hover:scale-105 hover:bg-gray-400" @click="closeEditOutfitForm">
                                Cancel
                            </button>
                            <button type="submit" class="w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md transform transition duration-300 hover:scale-105">
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            </form>
     
     <!-- Outfits Modal -->
    <div v-if="showOutfitsModal" @click.self="closeOutfitsModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto flex justify-center items-center z-40">
        <div class="bg-white p-6 rounded-lg shadow-lg w-[1000px]">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold">All Outfits</h2>
                <button @click="closeOutfitsModal" class="text-gray-500 hover:text-gray-700">
                    <span class="text-2xl">&times;</span>
                </button>
            </div>

            <!-- Search and Filter -->
            <div class="flex gap-4 mb-4">
                <input
                    type="text"
                    v-model="outfitSearchQuery"
                    placeholder="Search outfits..."
                    class="px-4 py-2 border rounded-lg flex-1"
                >
                <select 
                    v-model="outfitTypeFilter"
                    class="px-4 py-2 border rounded-lg"
                >
                    <option value="">All Types</option>
                    <option v-for="type in distinctOutfitTypes" :key="type" :value="type">
                        {{ type }}s
                    </option>
        </select>
     </div>       
    
    <!-- Outfits Table -->
        <div class="h-[400px] flex flex-col">
            <div class="overflow-x-auto flex-grow">
                <table class="w-full text-sm text-left">
                    <thead class="text-xs uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th scope="col" class="px-2 py-3 w-[5%]">#</th>
                            <th scope="col" class="px-2 py-3 w-[20%]">Name</th>
                            <th scope="col" class="px-2 py-3 w-[15%]">Type</th>
                            <th scope="col" class="px-2 py-3 w-[10%]">Color</th>
                            <th scope="col" class="px-2 py-3 w-[8%]">Size</th>
                            <th scope="col" class="px-2 py-3 w-[12%]">Price</th>
                            <th scope="col" class="px-2 py-3 w-[10%]">Status</th>
                            <th scope="col" class="px-2 py-3 w-[10%]">Image</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="outfit in paginatedOutfits" 
                            :key="outfit.outfit_id" 
                            class="bg-white border-b hover:bg-gray-50 cursor-pointer"
                            @click="openEditOutfit(outfit)">
                            <td class="px-2 py-3">{{ outfit.dummyIndex }}</td>
                            <td class="px-2 py-3 truncate">{{ outfit.outfit_name }}</td>
                            <td class="px-2 py-3 capitalize truncate">{{ outfit.outfit_type }}</td>
                            <td class="px-2 py-3 truncate">{{ outfit.outfit_color }}</td>
                            <td class="px-2 py-3">{{ outfit.size }}</td>
                            <td class="px-2 py-3">{{ formatPrice(outfit.rent_price) }} php</td>
                            <td class="px-2 py-3">
                                <span 
                                    :class="outfit.status === 'Available' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                                    class="px-2 py-1 rounded-full text-xs font-medium"
                                >
                                    {{ outfit.status }}
                                </span>
                            </td>
                            <td class="px-2 py-3">
                                <img 
                                    :src="getOutfitImageUrl(outfit.outfit_img)" 
                                    :alt="outfit.outfit_name"
                                    class="w-10 h-10 object-cover rounded"
                                    @error="handleImageError"
                                >
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div class="mt-4 flex justify-between items-center bg-white py-3 px-4">
                <div class="flex-1 flex justify-between sm:hidden">
                    <button 
                        @click="currentPage--" 
                        :disabled="currentPage === 1"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
                    >
                        Previous
                    </button>
                    <button 
                        @click="currentPage++" 
                        :disabled="currentPage >= totalPages"
                        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        :class="{ 'opacity-50 cursor-not-allowed': currentPage >= totalPages }"
                    >
                        Next
                    </button>
                </div>
                <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                    <div>
                        <p class="text-sm text-gray-700">
                            Showing
                            <span class="font-medium">{{ startIndex + 1 }}</span>
                            to
                            <span class="font-medium">{{ endIndex }}</span>
                            of
                            <span class="font-medium">{{ totalItems }}</span>
                            results
                        </p>
                    </div>
                    <div>
                        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                            <button 
                                @click="currentPage--" 
                                :disabled="currentPage === 1"
                                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
                            >
                                Previous
                            </button>
                            <button 
                                @click="currentPage++" 
                                :disabled="currentPage >= totalPages"
                                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                :class="{ 'opacity-50 cursor-not-allowed': currentPage >= totalPages }"
                            >
                                Next
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
        </div>
        </div>
            
    
          
    
    
    
    
    </div>

    <!-- Edit Outfit Form -->
    <form v-if="isEditingOutfit" @submit.prevent="handleEditSubmit" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-50 overflow-y-auto z-50" @click.self="closeEditOutfitForm">
        <div class="bg-white w-[1000px] p-5 rounded-lg shadow-lg overflow-y-auto">
            <div class="flex justify-between items-center m-3">
                <h1 class="font-semibold text-xl font-inter text-gray-800">Edit Outfit</h1>
            </div>
            <div class="border border-gray-500 mt-5 items-center"></div>
            <div class="m-5">
                <span>{{ errorMessage }}</span>

                <div class="flex flex-row gap-5">
                    <!-- Left Column - Input Fields -->
                    <div class="flex-1">
                        <!-- Outfit Name and Type -->
                        <div class="flex flex-row mt-5 gap-2">
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Outfit Name</label>
                    <input type="text" 
                                    class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                        v-model="editingOutfit.outfit_name" 
                        required>
                            </div>
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Outfit Type</label>
                                <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                            v-model="editingOutfit.outfit_type" 
                            required>
                                    <option value="" disabled selected>Select Type</option>
                        <option value="Wedding Gown">Wedding Gown</option>
                        <option value="Saree">Saree</option>
                        <option value="Lehenga">Lehenga</option>
                        <option value="Suit">Suit</option>
                        <option value="Gown">Gown</option>
                        <option value="Jumpsuit">Jumpsuit</option>
                        <option value="Reception Dress">Reception Dress</option>
                        <option value="Bridal Robe">Bridal Robe</option>
                        <option value="Tuxedo">Tuxedo</option>
                        <option value="Sherwani">Sherwani</option>
                        <option value="Kurta Pajama">Kurta Pajama</option>
                        <option value="Bespoke Tailored Outfit">Bespoke Tailored Outfit</option>
                        <option value="Barong Tagalog">Barong Tagalog</option>
                        <option value="Morning Coat">Morning Coat</option>
                        <option value="Bridesmaid Dress">Bridesmaid Dress</option>
                        <option value="Cultural Attire">Cultural Attire</option>
                        <option value="Mix-and-Match Dress">Mix-and-Match Dress</option>
                        <option value="Flower Girl Dress">Flower Girl Dress</option>
                        <option value="Ring Bearer Suit">Ring Bearer Suit</option>
                        <option value="Formal Attire">Formal Attire</option>
                        <option value="Semi-Formal Attire">Semi-Formal Attire</option>
                        <option value="Traditional/Tribal Wear">Traditional/Tribal Wear</option>
                        <option value="Engagement Outfit">Engagement Outfit</option>
                        <option value="Rehearsal Dinner Attire">Rehearsal Dinner Attire</option>
                        <option value="Haldi Ceremony Outfit">Haldi Ceremony Outfit</option>
                        <option value="Mehndi Ceremony Outfit">Mehndi Ceremony Outfit</option>
                        <option value="Cocktail Party Wear">Cocktail Party Wear</option>
                        <option value="Destination Wedding Attire">Destination Wedding Attire</option>
                        <option value="Seasonal Attire">Seasonal Attire</option>
                    </select>
                            </div>
                </div>

                        <!-- Color and Price -->
                        <div class="flex flex-row mt-5 gap-2">
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Outfit Color</label>
                                <input type="text" 
                                    class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                    v-model="editingOutfit.outfit_color" placeholder="Outfit Color" required>
                            </div>
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Rent Price</label>
                                <input type="number" step="0.01" class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                    v-model="editingOutfit.rent_price" placeholder="Rent Price" required>
                            </div>
                </div>

                        <!-- Size and Weight -->
                        <div class="flex flex-row mt-5 gap-2">
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Size</label>
                                <select class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                    v-model="editingOutfit.size" required>
                                    <option value="" disabled selected>Select Size</option>
                        <option value="XS">XS</option>
                        <option value="S">S</option>
                        <option value="M">M</option>
                        <option value="L">L</option>
                        <option value="XL">XL</option>
                        <option value="2XL">2XL</option>
                        <option value="3XL">3XL</option>
                        <option value="4XL">4XL</option>
                        <option value="5XL">5XL</option>
                    </select>
                            </div>
                            <div class="w-full">
                                <label class="text-xs text-gray-600 mb-2 block">Weight (kg)</label>
                                <input type="number" step="0.01" class="p-2 w-full h-10 rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                    v-model="editingOutfit.weight" placeholder="Weight" required>
                            </div>
                </div>

                <!-- Status Toggle -->
                <div class="flex flex-row mt-5 items-center">
                            <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" 
                               v-model="editingOutfit.status" 
                               :true-value="'Available'" 
                               :false-value="'Unavailable'" 
                               class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer 
                                  peer-checked:after:translate-x-full peer-checked:after:border-white 
                                  after:content-[''] after:absolute after:top-[2px] after:left-[2px] 
                                  after:bg-white after:border-gray-300 after:border after:rounded-full 
                                  after:h-5 after:w-5 after:transition-all 
                                  peer-checked:bg-green-600"></div>
                        <span class="ml-3 text-sm font-medium text-gray-900">
                            {{ editingOutfit.status }}
                        </span>
                    </label>
                </div>
                
                        <!-- Description -->
                <div class="flex flex-col mt-5">
                            <label class="text-xs text-gray-600 mb-2">Outfit Description</label>
                            <textarea class="p-2 w-full rounded-lg shadow-md border border-gray-500 focus:outline-none focus:border-blue-700" 
                                v-model="editingOutfit.outfit_desc" placeholder="Description" rows="4" required></textarea>
                        </div>
                </div>

                    <!-- Right Column - Image Upload -->
                    <div class="w-2/5">
                        <div class="flex flex-col">
                            <label class="text-xs text-gray-600 mb-2">Outfit Image</label>
                            <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                <!-- Image Preview -->
                                <div v-if="editImagePreview" class="mb-4">
                                    <img :src="editImagePreview" alt="Outfit Preview" class="max-w-full h-auto rounded-lg mx-auto mb-4">
                                </div>
                                <!-- Upload Button -->
                                <label class="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600 inline-block">
                                    <span>{{ editImagePreview ? 'Change Image' : 'Choose Image' }}</span>
                            <input type="file" class="hidden" @change="onEditFileSelected" accept="image/*" ref="editFileInput">
                        </label>
                                <p class="mt-2 text-sm text-gray-500">{{ editingSelectedFileName || 'No file chosen' }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Buttons -->
                <div class="flex justify-end items-center mt-5 space-x-2">
                    <button class="w-20 h-10 bg-gray-300 text-white px-3 py-1 rounded transform transition duration-300 hover:scale-105 hover:bg-gray-400" @click="closeEditOutfitForm">
                        Cancel
                    </button>
                    <button type="submit" class="w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md transform transition duration-300 hover:scale-105">
                        Save
                    </button>
                </div>
            </div>
        </div>
    </form>
    </template>
    
    <script>
    import axios from 'axios';
    
    
    axios.defaults.withCredentials = true;
    
    export default {
        name: 'AddOutfitPackage',
        data() {
            return {
            showTable: 'GownPackages',
            currentGownPackagePage: 1,
            rowsPerGownPackagePage: 5,
            editGownPackageForm: false,
			addOutfitForm: false,
			searchTerm: '',
            newGownPackage: {
                gown_package_name: '',
                description: '',
                outfits: []
            },
            gownPackages: [],
            addOutfitsPackageForm: false,
            gowns: [],
            tuxedos: [],
            errorMessage: '',
            selectedGowns: [],
            selectedTuxedos: [],
            selectedGownPackage: {
                gown_package_id: null,
                gown_package_name: '',
                gown_package_price: '',
                description: '',
                selectedGowns: [],
                selectedTuxedos: []
            },
            editDiscount: 0,
            newOutfit: {
                outfit_name: '',
                outfit_type: '',
                outfit_color: '',
                outfit_desc: '',
                rent_price: '',
                status: 'Available',
                outfit_img: '',
                size: '',
                weight: ''
            },
            outfitArchive: {
                creation_address: '',
                owner: ''
            },
          
            previewSrc: null,
            previewImage: "",

            showOutfitModal: false,
                currentOutfitType: '', // 'gown' or 'tuxedo'
                packageDetails: {
                    name: '',
                    description: ''
                },
            selectedOutfits: [],

            showModal: false,
                modalType: null,
                inclusions: [],
                packageDetails: {
                    name: '',
                    description: '',
                    outfits: [],
                    discount: 0,
                },

            showOutfitPackageForm: false,
            outfitSearchTerm: '',
            showOutfitModal: false,
            searchQuery: '',
            outfits: [],

            packageInclusions: [],
            packageDetails: {
                name: '',
                description: '',
                discount: 0
            },
            showStatusConfirmModal: false,
            pendingStatus: '',
            selectedPackage: null,
            isInactivePackagesModalVisible: false,
            inactivePackages: [],

            showOutfitsModal: false,
            outfitSearchQuery: '',
            outfitTypeFilter: '',
            currentPage: 1,
            rowsPerPage: 5,
            
            // Selection mode for the outfit modal ('add' or 'edit')
            outfitSelectionMode: 'add',
            
            // Image upload properties
            selectedFileName: null,
            apiBaseUrl: 'http://127.0.0.1:5000',

            // Edit mode properties
            isEditingOutfit: false,
            editingOutfit: null,
            editingOutfitArchive: {
                archive_id: null,
                outfit_id: null,
                creation_address: '',
                creation_date: '',
                owner: '',
                retail_price: '',
                usage: 0
            },
            editingSelectedFileName: null,
            
            // Image upload properties
            selectedFile: null,
            editingSelectedFile: null,
            showAlert: false,
            alertType: 'success',
            alertMessage: '',
            imagePreview: null,
            editImagePreview: null,
        };
    },

     computed: {
        totalOutfitPackages() {
            return this.gownPackages.length;
        },
        paginatedGownPackages() {
            const start = (this.currentGownPackagePage - 1) * this.rowsPerGownPackagePage;
            const end = start + this.rowsPerGownPackagePage;
            return this.gownPackages.slice(start, end);
        },
        totalGownPackagePages() {
            return Math.ceil(this.gownPackages.length / this.rowsPerGownPackagePage);
        },
        filteredOutfits() {
            if (!this.searchQuery) return this.outfits;
            
            const query = this.searchQuery.toLowerCase();
            return this.outfits.filter(outfit => 
                outfit.outfit_name.toLowerCase().includes(query) || 
                outfit.outfit_type.toLowerCase().includes(query) ||
                outfit.outfit_color.toLowerCase().includes(query)
            );
        },
        filteredOutfitsForModal() {
            return this.outfits.filter(outfit => {
                // Filter by search query
                const matchesSearch = !this.outfitSearchQuery || 
                    outfit.outfit_name.toLowerCase().includes(this.outfitSearchQuery.toLowerCase()) ||
                                    outfit.outfit_type.toLowerCase().includes(this.outfitSearchQuery.toLowerCase()) ||
                                    outfit.outfit_color.toLowerCase().includes(this.outfitSearchQuery.toLowerCase());
                
                // Filter by outfit type
                const matchesType = !this.outfitTypeFilter || 
                    outfit.outfit_type === this.outfitTypeFilter;
                
                return matchesSearch && matchesType;
            });
        },

        totalItems() {
            return this.filteredOutfitsForModal.length;
        },
        totalPages() {
            return Math.ceil(this.totalItems / this.rowsPerPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.rowsPerPage;
        },
        endIndex() {
            return Math.min(this.startIndex + this.rowsPerPage, this.totalItems);
        },
        paginatedOutfits() {
            return this.filteredOutfitsForModal.slice(this.startIndex, this.endIndex);
        },
        
        // New computed property for the Update Package form
        selectedPackageOutfits() {
            if (!this.selectedGownPackage) return [];
            
            // Combine selected gowns and tuxedos into a single array
            const selectedGownIds = this.selectedGownPackage.selectedGowns || [];
            const selectedTuxedoIds = this.selectedGownPackage.selectedTuxedos || [];
            
            // Get the actual outfit objects that match the selected IDs
            const selectedGowns = selectedGownIds.map(id => 
                this.gowns.find(outfit => outfit.outfit_id === id)
            ).filter(outfit => outfit); // Remove undefined values
            
            const selectedTuxedos = selectedTuxedoIds.map(id => 
                this.tuxedos.find(outfit => outfit.outfit_id === id)
            ).filter(outfit => outfit); // Remove undefined values
            
            // Combine both arrays
            return [...selectedGowns, ...selectedTuxedos];
        },
        distinctOutfitTypes() {
            // Extract unique outfit types from the outfits array
            const types = new Set(this.outfits.map(outfit => outfit.outfit_type));
            return Array.from(types).sort();
        }
    },
    methods: {
        async fetchGownPackages() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    alert('You are not logged in. Please log in to view gown packages.');
                    return;
                }
        
                const response = await axios.get('http://127.0.0.1:5000/gown-packages', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    withCredentials: true
                });
        
                // Populate gownPackages array with data from API
                this.gownPackages = response.data.map((item, index) => ({
                    gown_package_id: item.gown_package_id,
                    gown_package_name: item.gown_package_name,
                    gown_package_price: item.gown_package_price,
                    description: item.description,
                    status: item.status || 'Active', // Add status field
                    dummyIndex: index + 1,
                }));
        
            } catch (error) {
                console.error('Error fetching gown packages:', error.response?.data || error.message);
            }
        },

        // Add calculation methods
        calculateSubtotal() {
            return this.packageInclusions.reduce((total, item) => {
                return total + parseFloat(item.rent_price || 0);
            }, 0);
        },

        calculateDiscount() {
            const subtotal = this.calculateSubtotal();
            const discountPercentage = parseFloat(this.packageDetails.discount || 0);
            return (subtotal * discountPercentage) / 100;
        },

        calculateTotal() {
            return this.calculateSubtotal() - this.calculateDiscount();
        },
        
        // Add close package form method
        closePackageForm() {
            this.showOutfitPackageForm = false;
            this.packageDetails = {
                name: '',
                description: '',
                discount: 0
            };
            this.packageInclusions = [];
            this.selectedOutfits = [];
            this.errorMessage = '';
        },

    async fetchOutfits() {
            try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                alert('You are not logged in. Please log in to view outfits.');
                return;
            }

            const response = await axios.get('http://127.0.0.1:5000/outfits', {
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                },
                withCredentials: true,
            });

            // Populate outfits array with data from API
            this.outfits = response.data.map((item, index) => ({
                outfit_id: item.outfit_id,
                outfit_name: item.outfit_name,
                outfit_type: item.outfit_type,
                outfit_color: item.outfit_color,
                outfit_desc: item.outfit_desc,
                rent_price: item.rent_price,
                status: item.status,
                outfit_img: item.outfit_img,
                size: item.size,
                weight: item.weight,
                creation_address: item.creation_address,
                owner: item.owner,
                archive_id: item.archive_id,
                dummyIndex: index + 1,
            }));

            // Separate outfits by type - include more dress-related terms
            const dressTerms = ['gown', 'dress', 'robe', 'bridesmaid'];
            this.gowns = this.outfits.filter(outfit => 
                dressTerms.some(term => outfit.outfit_type.toLowerCase().includes(term))
            );
            this.tuxedos = this.outfits.filter(outfit => 
                !dressTerms.some(term => outfit.outfit_type.toLowerCase().includes(term))
            );

            } catch (error) {
            console.error('Error fetching outfits:', error.response?.data || error.message);
            }
        },
        addGownOutfits(event) {
            const selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
            this.newGownPackage.outfits = [...new Set([...this.newGownPackage.outfits, ...selectedOptions])];
        },
        addTuxedoOutfits(event) {
            const selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
            this.newGownPackage.outfits = [...new Set([...this.newGownPackage.outfits, ...selectedOptions])];
        },

    
        async submitPackage() {
                try {
                    const token = localStorage.getItem('access_token');
                    if (!token) {
                        this.showAlertMessage('You are not logged in. Please log in to add a package.', 'error');
                        return;
                    }

                    if (!this.packageDetails.name) {
                        this.showAlertMessage('Please enter a package name', 'error');
                        return;
                    }

                    if (this.packageInclusions.length === 0) {
                        this.showAlertMessage('Please add at least one outfit to the package', 'error');
                        return;
                    }

                    const packageData = {
                        gown_package_name: this.packageDetails.name,
                        description: this.packageDetails.description || '',
                        outfits: this.packageInclusions.map(item => item.outfit_id),
                        discount: this.packageDetails.discount || 0
                    };

                    const response = await axios.post('http://127.0.0.1:5000/add-gown-package', packageData, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`,
                        },
                        withCredentials: true,
                    });

                    this.showAlertMessage('Package added successfully');
                    
                    // Reset form
                    this.packageDetails = {
                        name: '',
                        description: '',
                        discount: 0
                    };
                    this.packageInclusions = [];
                    this.selectedOutfits = [];
                    this.showOutfitPackageForm = false;
                } catch (error) {
                    console.error('Error details:', {
                        message: error.message,
                        response: error.response?.data,
                        status: error.response?.status
                    });
                    this.showAlertMessage(error.response?.data?.message || 'An error occurred. Please try again.', 'error');
                }
            },
        updateFileName(event) {
            const fileInput = event.target;
            const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : "No file selected";
            document.getElementById("displayFileName").textContent = fileName;
        },



            
        // Pagination methods
        prevGownPackagePage() {
            if (this.currentGownPackagePage > 1) {
                this.currentGownPackagePage--;
            }
        },
        nextGownPackagePage() {
            if (this.currentGownPackagePage < this.totalGownPackagePages) {
                this.currentGownPackagePage++;
            }
        },
        changeGownPackagePage(page) {
            this.currentGownPackagePage = page;
        },
        editVenueBtn(index) {
            // Handle edit action for venue
            console.log(`Edit venue at index: ${index}`);
        },
    
        addOutfitsPackageBtn() {
            this.showOutfitPackageForm = true;  // Show the form
            this.packageDetails = {
                name: '',
                description: ''
            };
            this.inclusions = [];
        },
        closeAddGownPackageForm()
        {
            this.addOutfitsPackageForm = false;
            this.newGownPackage = {};
        },
       
        formatPrice(price) {
            if (price === null || price === undefined || typeof price === 'object' || isNaN(price)) {
                return 'N/A'; // Return a fallback if price is invalid
            }
            // Ensure price is treated as a number, round to 2 decimal places, and format with commas
            return parseFloat(price).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
            },
            
            editGownPackageBtn(index) {
                const gownPackage = this.paginatedGownPackages[index];
                
                // Initialize the form with the package data
                this.selectedGownPackage = {
                    gown_package_id: gownPackage.gown_package_id,
                    gown_package_name: gownPackage.gown_package_name,
                    gown_package_price: gownPackage.gown_package_price,
                    description: gownPackage.description,
                    selectedGowns: [],
                    selectedTuxedos: []
                };
                
                // Reset the edit discount
                this.editDiscount = 0;
                
                // Fetch the package outfits from backend
                this.fetchPackageOutfits(gownPackage.gown_package_id);
                
                // Show the edit form
                this.editGownPackageForm = true;
            },
            
            async fetchPackageOutfits(packageId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const response = await axios.get(`http://127.0.0.1:5000/gown-package-outfits/${packageId}`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    if (response.data && Array.isArray(response.data)) {
                        // Sort outfits into gowns and tuxedos
                        response.data.forEach(outfit => {
                            const outfitType = outfit.outfit_type.toLowerCase();
                            if (outfitType.includes('gown') || outfitType.includes('dress')) {
                                this.selectedGownPackage.selectedGowns.push(outfit.outfit_id);
                            } else {
                                this.selectedGownPackage.selectedTuxedos.push(outfit.outfit_id);
                            }
                        });
                    }
                } catch (error) {
                    console.error('Error fetching package outfits:', error);
                    this.errorMessage = 'Failed to load package outfits';
                }
            },

            closeEditGownPackageForm() {
                this.editGownPackageForm = false;
                this.selectedGownPackage = {
                    gown_package_name: '',
                    description: '',
                    gown_ids: [],
                    tuxedo_ids: []
                }; // Reset form fields to default
                this.errorMessage = ''; // Clear error messages
                },

            // New methods for Update Outfit Package form
            removeOutfitFromPackage(outfitId) {
                // Check if we're in edit mode
                if (this.editGownPackageForm) {
                    // Remove from selectedGowns array
                const gownIndex = this.selectedGownPackage.selectedGowns.indexOf(outfitId);
                if (gownIndex !== -1) {
                    this.selectedGownPackage.selectedGowns.splice(gownIndex, 1);
                }
                
                    // Remove from selectedTuxedos array
                const tuxedoIndex = this.selectedGownPackage.selectedTuxedos.indexOf(outfitId);
                if (tuxedoIndex !== -1) {
                    this.selectedGownPackage.selectedTuxedos.splice(tuxedoIndex, 1);
                    }
                } else {
                    // Regular mode (Add Package form)
                    // Remove from packageInclusions
                    const inclusionIndex = this.packageInclusions.findIndex(item => item.outfit_id === outfitId);
                    if (inclusionIndex !== -1) {
                        this.packageInclusions.splice(inclusionIndex, 1);
                    }
                    
                    // Remove from selectedOutfits
                    const outfitIndex = this.selectedOutfits.findIndex(item => item.outfit_id === outfitId);
                    if (outfitIndex !== -1) {
                        this.selectedOutfits.splice(outfitIndex, 1);
                    }
                }
            },
            
            openEditOutfitSelection() {
                // Set up a flag to indicate we're in edit mode for outfit selection
                this.outfitSelectionMode = 'edit';
                
                // Open the outfit selection modal
                this.showOutfitModal = true;
                },

			addOutfitsBtn() {
				this.addOutfitForm = true;
			},
            closeAddOutfitForm() {
                this.addOutfitForm = false;
            },

            onFileSelected(event) {
                const file = event.target.files[0];
                if (file) {
                    this.selectedFile = file;
                    this.selectedFileName = file.name;
                    // Create preview URL
                    this.imagePreview = URL.createObjectURL(file);
                }
            },

            async handleSubmit() {
                try {
                    this.isLoading = true;
                    const token = localStorage.getItem('access_token');

                    if (!this.newOutfit.outfit_name || !this.newOutfit.outfit_type || !this.newOutfit.outfit_color || 
                        !this.newOutfit.rent_price || !this.newOutfit.size || !this.newOutfit.weight) {
                        this.showAlertMessage('Please fill in all required fields', 'error');
                      this.isLoading = false;
                      return;
                    }

                    if (this.selectedFile) {
                      // If a file is selected, use FormData
                      const formData = new FormData();
                      formData.append('outfit_name', this.newOutfit.outfit_name);
                      formData.append('outfit_type', this.newOutfit.outfit_type);
                      formData.append('outfit_color', this.newOutfit.outfit_color);
                      formData.append('outfit_desc', this.newOutfit.outfit_desc || '');
                      formData.append('rent_price', this.newOutfit.rent_price);
                      formData.append('size', this.newOutfit.size);
                      formData.append('weight', this.newOutfit.weight);
                      formData.append('status', 'Available');
                      
                      // Create archive data as a nested object
                      const archiveData = {
                        creation_address: this.outfitArchive.creation_address || '',
                        owner: this.outfitArchive.owner || ''
                      };
                      
                      // Add archive data as a JSON string
                      formData.append('archive', JSON.stringify(archiveData));
                      
                      // Add the file
                      formData.append('outfit_image', this.selectedFile);
                      
                      // Send request to API
                      const response = await axios.post('http://127.0.0.1:5000/outfits', formData, {
                        headers: {
                          'Content-Type': 'multipart/form-data',
                          'Authorization': `Bearer ${token}`
                        }
                      });
                      
                      this.selectedFileName = null;
                      
                      this.showAlertMessage('Outfit added successfully');
                      this.addOutfitForm = false;
                        this.resetForm();
                    } else {
                      // If no file is selected, send as JSON
                      const outfitData = {
                        outfit_name: this.newOutfit.outfit_name,
                        outfit_type: this.newOutfit.outfit_type,
                        outfit_color: this.newOutfit.outfit_color,
                        outfit_desc: this.newOutfit.outfit_desc || '',
                        rent_price: this.newOutfit.rent_price,
                        size: this.newOutfit.size,
                        weight: this.newOutfit.weight,
                        status: 'Available',
                        archive: {
                          creation_address: this.outfitArchive.creation_address || '',
                          owner: this.outfitArchive.owner || ''
                        }
                      };
                      
                      // Send request to API
                      const response = await axios.post('http://127.0.0.1:5000/outfits', outfitData, {
                        headers: {
                          'Content-Type': 'application/json',
                          'Authorization': `Bearer ${token}`
                        }
                      });
                      
                      this.showAlertMessage('Outfit added successfully');
                      this.addOutfitForm = false;
                      this.resetForm();
                    }
                } catch (error) {
                    console.error('Error adding outfit:', error);
                    if (error.response) {
                      if (error.response.status === 413) {
                            this.showAlertMessage('File size is too large. Please choose a smaller file.', 'error');
                      } else if (error.response.status === 401) {
                            this.showAlertMessage('Unauthorized. Please log in again.', 'error');
                        } else {
                            this.showAlertMessage(error.response.data.message || 'Error adding outfit. Please try again.', 'error');
                      }
                    } else if (error.request) {
                        this.showAlertMessage('No response from server. Please try again later.', 'error');
                    } else {
                        this.showAlertMessage('Error adding outfit. Please try again.', 'error');
                    }
                  } finally {
                    this.isLoading = false;
                }
            },

            resetForm() {
                this.newOutfit = {
                    outfit_name: '',
                    outfit_type: '',
                    outfit_color: '',
                    outfit_desc: '',
                    rent_price: '',
                    size: '',
                    weight: ''
                };
                this.outfitArchive = {
                    creation_address: '',
                    owner: ''
                };
                this.selectedFile = null;
                this.selectedFileName = null;
                this.errorMessage = '';
                this.isLoading = false;
                this.imagePreview = null;
            },

            openOutfitSelection(type) {
                this.currentOutfitType = type;
                this.showOutfitModal = true;
            },
            closeOutfitModal() {
                this.showOutfitModal = false;
                this.searchQuery = '';
                // Reset the selection mode when closing the modal
                this.outfitSelectionMode = 'add';
            },
   
 
            isOutfitSelected(outfitId) {
                // Check if we're in edit mode for the Update Package form
                if (this.outfitSelectionMode === 'edit' && this.selectedGownPackage) {
                    // Check both arrays for the outfit ID
                    return this.selectedGownPackage.selectedGowns.includes(outfitId) || 
                           this.selectedGownPackage.selectedTuxedos.includes(outfitId);
                }
                
                // Regular mode (Add Package form)
                return this.selectedOutfits.some(outfit => outfit.outfit_id === outfitId);
            },
            toggleOutfitSelection(outfit) {
                // Check if we're in edit mode for the Update Package form
                if (this.outfitSelectionMode === 'edit') {
                    // Determine outfit type
                    const isGown = outfit.outfit_type.toLowerCase().includes('gown') || 
                        outfit.outfit_type.toLowerCase().includes('dress');
                    
                    // Check if this outfit is already selected
                    const targetArray = isGown ? 'selectedGowns' : 'selectedTuxedos';
                    const isSelected = this.selectedGownPackage[targetArray].includes(outfit.outfit_id);
                    
                    if (isSelected) {
                        // Remove the outfit if already selected
                        const index = this.selectedGownPackage[targetArray].indexOf(outfit.outfit_id);
                        if (index !== -1) {
                            this.selectedGownPackage[targetArray].splice(index, 1);
                        }
                    } else {
                        // Add the outfit if not selected
                        this.selectedGownPackage[targetArray].push(outfit.outfit_id);
                    }
                    
                    // Close the modal
                    this.closeOutfitModal();
                    return;
                }
                
                // Regular mode (Add Package form)
                const index = this.selectedOutfits.findIndex(item => item.outfit_id === outfit.outfit_id);
                if (index === -1) {
                    // Add to selectedOutfits array
                    this.selectedOutfits.push(outfit);
                    
                    // Add to packageInclusions
                    this.packageInclusions.push({
                        outfit_id: outfit.outfit_id,
                        outfit_type: outfit.outfit_type,
                        outfit_name: outfit.outfit_name,
                        rent_price: outfit.rent_price
                    });
                } else {
                    // Remove from selectedOutfits array
                    this.selectedOutfits.splice(index, 1);
                    
                    // Remove from packageInclusions
                    const inclusionIndex = this.packageInclusions.findIndex(item => item.outfit_id === outfit.outfit_id);
                    if (inclusionIndex !== -1) {
                        this.packageInclusions.splice(inclusionIndex, 1);
                    }
                }
                
                // Close the modal after selection
                this.closeOutfitModal();
            },
    
            async togglePackageStatus(packages) {
                try {
                    const token = localStorage.getItem('access_token');
                    const response = await axios.put(
                        `http://127.0.0.1:5000/toggle-package-status/${packages.gown_package_id}`,
                        {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );

                    if (response.status === 200) {
                        alert("Package status updated successfully!");
                        await this.fetchPackages();
                        await this.fetchInactivePackages();
                        if (this.showInactivePackagesModal) {
                            this.closeInactivePackagesModal();
                        }
                    }
                } catch (error) {
                    console.error('Error toggling package status:', error);
                    alert('Failed to update package status. Please try again.');
                }
            },

            async fetchInactivePackages() {
                try {
                    const token = localStorage.getItem('access_token');
                    const response = await axios.get('http://127.0.0.1:5000/inactive-gown-packages', {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    this.inactivePackages = response.data;
                } catch (error) {
                    console.error('Error fetching inactive packages:', error);
                }
            },


            openStatusConfirmModal(gownPackage, newStatus) {
                this.selectedPackage = gownPackage;
                this.pendingStatus = newStatus;
                this.showStatusConfirmModal = true;
            },

            async togglePackageStatus() {
                if (!this.selectedPackage) return;
                
                try {
                    const token = localStorage.getItem('access_token');
                    await axios.put(`http://127.0.0.1:5000/toggle-gown-package-status/${this.selectedPackage.gown_package_id}`, {}, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    // Refresh both active and inactive packages
                    await this.fetchGownPackages();
                    await this.fetchInactivePackages();
                    this.closeStatusConfirmModal();
                } catch (error) {
                    console.error('Error toggling package status:', error);
                }
            },

            closeStatusConfirmModal() {
                this.showStatusConfirmModal = false;
                this.selectedPackage = null;
                this.pendingStatus = '';
            },

            async confirmStatusChange() {
                if (this.selectedPackage) {
                    await this.togglePackageStatus(this.selectedPackage);
                    this.closeStatusConfirmModal();
                }
            },

            showInactivePackagesModal() {
                this.fetchInactivePackages();
                this.isInactivePackagesModalVisible = true;
            },
            closeInactivePackagesModal() {
                this.isInactivePackagesModalVisible = false;
            },
    
            showOutfitsModalFn() {
                this.showOutfitsModal = true;
                this.fetchOutfits();
            },
            closeOutfitsModal() {
                this.showOutfitsModal = false;
                this.outfitSearchQuery = '';
                this.outfitTypeFilter = '';
                this.currentPage = 1; // Reset pagination
            },

            async updateGownPackage() {
                try {
                    const token = localStorage.getItem('access_token');
                    
                    if (!this.selectedGownPackage.gown_package_name) {
                        this.showAlertMessage('Please enter a package name', 'error');
                        return;
                    }
                    
                    // Calculate the total price
                    const totalPrice = this.calculateEditTotal();
                    
                    // Create the package data to send
                    const packageData = {
                        gown_package_name: this.selectedGownPackage.gown_package_name,
                        description: this.selectedGownPackage.description || '',
                        gown_package_price: totalPrice,
                        outfit_ids: [
                            ...this.selectedGownPackage.selectedGowns,
                            ...this.selectedGownPackage.selectedTuxedos
                        ]
                    };
                    
                    console.log('Updating package with data:', packageData);
                    
                    const response = await axios.put(
                        `http://127.0.0.1:5000/update-gown-package/${this.selectedGownPackage.gown_package_id}`,
                        packageData,
                        {
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`
                            }
                        }
                    );
                    
                    if (response.status === 200) {
                        this.showAlertMessage('Package updated successfully');
                        this.closeEditGownPackageForm();
                        this.fetchGownPackages(); // Refresh the packages list
                    }
                } catch (error) {
                    console.error('Error updating package:', error);
                    this.showAlertMessage(error.response?.data?.message || 'Failed to update package', 'error');
                }
            },

        calculateEditSubtotal() {
            return this.selectedPackageOutfits.reduce((total, item) => {
                return total + parseFloat(item.rent_price || 0);
            }, 0);
        },

        calculateEditDiscount() {
            const subtotal = this.calculateEditSubtotal();
            const discountPercentage = parseFloat(this.editDiscount || 0);
            return (subtotal * discountPercentage) / 100;
        },

        calculateEditTotal() {
            return this.calculateEditSubtotal() - this.calculateEditDiscount();
        },

        getOutfitImageUrl(imageFileName) {
            // If the outfit has an image
            if (imageFileName && imageFileName.length > 0) {
                // Check if it's a full URL or just a path
                if (imageFileName.startsWith('http')) {
                    return imageFileName;
                } else {
                    // Use the API endpoint for outfit images with a cache busting parameter
                    const timestamp = new Date().getTime();
                    return `${this.apiBaseUrl}/api/outfit-image/${imageFileName}?t=${timestamp}`;
                }
            }
            
            // Default fallback - just return empty string to avoid errors
            return '';
        },
        
        handleImageError(e) {
            // Don't try to load a placeholder, just hide the broken image
            e.target.style.display = 'none';
        },
    
        async openEditOutfit(outfit) {
          try {
            this.isEditingOutfit = true;
            this.editingOutfit = { ...outfit };
            this.errorMessage = '';
            
            // Set the image preview if outfit has an image
            if (outfit.outfit_img) {
                this.editImagePreview = this.getOutfitImageUrl(outfit.outfit_img);
            }
            
            // Fetch the outfit archive data
            const token = localStorage.getItem('access_token');
            try {
              const response = await axios.get(`http://127.0.0.1:5000/outfits/${outfit.outfit_id}/archive`, {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              
              if (response.data) {
                // If archive data is returned, use it
                this.editingOutfitArchive = {
                  archive_id: response.data.archive_id || null,
                  outfit_id: outfit.outfit_id,
                  creation_address: response.data.creation_address || '',
                  owner: response.data.owner || ''
                };
              } else {
                // If no archive data is returned, use default values
                this.editingOutfitArchive = {
                  archive_id: null,
                  outfit_id: outfit.outfit_id,
                  creation_address: '',
                  owner: ''
                };
              }
            } catch (error) {
              console.error('Error fetching outfit archive data:', error);
              // If there's an error fetching the archive data, use any available archive data from the outfit object
              this.editingOutfitArchive = {
                archive_id: outfit.archive_id || null,
                outfit_id: outfit.outfit_id,
                creation_address: outfit.creation_address || '',
                owner: outfit.owner || ''
              };
            }
            
            this.editingSelectedFileName = null;
          } catch (error) {
            console.error('Error opening edit form:', error);
            this.errorMessage = 'Error opening edit form. Please try again.';
          }
        },

        closeEditOutfitForm() {
            this.isEditingOutfit = false;
            this.editingOutfit = null;
            this.editingOutfitArchive = null;
            this.editingSelectedFileName = null;
            this.errorMessage = '';
        },

        onEditFileSelected(event) {
            const file = event.target.files[0];
            if (file) {
                this.editingSelectedFile = file;
                this.editingSelectedFileName = file.name;
                // Create preview URL
                this.editImagePreview = URL.createObjectURL(file);
            }
        },

        async handleEditSubmit() {
            try {
                this.isLoading = true;
                const token = localStorage.getItem('access_token');

                if (!this.editingOutfit.outfit_name || !this.editingOutfit.outfit_type || !this.editingOutfit.outfit_color || 
                    !this.editingOutfit.rent_price || !this.editingOutfit.size || !this.editingOutfit.weight) {
                    this.showAlertMessage('Please fill in all required fields', 'error');
                  this.isLoading = false;
                  return;
                }

                console.log("Selected file:", this.editingSelectedFile);
                
                if (this.editingSelectedFile) {
                  // If a file is selected, use FormData
                  const formData = new FormData();
                  formData.append('outfit_id', this.editingOutfit.outfit_id);
                  formData.append('outfit_name', this.editingOutfit.outfit_name);
                  formData.append('outfit_type', this.editingOutfit.outfit_type);
                  formData.append('outfit_color', this.editingOutfit.outfit_color);
                  formData.append('outfit_desc', this.editingOutfit.outfit_desc || '');
                  formData.append('rent_price', this.editingOutfit.rent_price);
                  formData.append('size', this.editingOutfit.size);
                  formData.append('weight', this.editingOutfit.weight);
                  formData.append('status', this.editingOutfit.status || 'Available');
                  
                  // Create archive data as a nested object
                  const archiveData = {
                    archive_id: this.editingOutfitArchive.archive_id,
                    outfit_id: this.editingOutfit.outfit_id,
                    creation_address: this.editingOutfitArchive.creation_address || '',
                    owner: this.editingOutfitArchive.owner || ''
                  };
                  
                  // Add archive data as a JSON string
                  formData.append('archive', JSON.stringify(archiveData));
                  
                  // Add the file - make sure to use the correct field name expected by the backend
                  formData.append('outfit_image', this.editingSelectedFile);
                  
                  // Send request to API
                  const response = await axios.put(`http://127.0.0.1:5000/outfits/${this.editingOutfit.outfit_id}`, formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data',
                      'Authorization': `Bearer ${token}`
                    }
                  });
                  
                  this.editingSelectedFileName = null;
                  
                  this.showAlertMessage('Outfit updated successfully');
                  this.isEditingOutfit = false;
                  this.resetEditForm();
                  await this.fetchOutfits(); // Refresh the outfits list
                } else {
                  // If no file is selected, send as JSON
                  const outfitData = {
                    outfit_id: this.editingOutfit.outfit_id,
                    outfit_name: this.editingOutfit.outfit_name,
                    outfit_type: this.editingOutfit.outfit_type,
                    outfit_color: this.editingOutfit.outfit_color,
                    outfit_desc: this.editingOutfit.outfit_desc || '',
                    rent_price: this.editingOutfit.rent_price,
                    size: this.editingOutfit.size,
                    weight: this.editingOutfit.weight,
                    status: this.editingOutfit.status || 'Available',
                    archive: {
                      archive_id: this.editingOutfitArchive.archive_id,
                      outfit_id: this.editingOutfit.outfit_id,
                      creation_address: this.editingOutfitArchive.creation_address || '',
                      owner: this.editingOutfitArchive.owner || ''
                    }
                  };
                  
                  // Send request to API
                  const response = await axios.put(`http://127.0.0.1:5000/outfits/${this.editingOutfit.outfit_id}`, outfitData, {
                    headers: {
                      'Content-Type': 'application/json',
                      'Authorization': `Bearer ${token}`
                    }
                  });
                  
                  this.showAlertMessage('Outfit updated successfully');
                  this.isEditingOutfit = false;
                  this.resetEditForm();
                  await this.fetchOutfits(); // Refresh the outfits list
                }
              } catch (error) {
                console.error('Error updating outfit:', error);
                if (error.response) {
                  if (error.response.status === 413) {
                        this.showAlertMessage('File size is too large. Please choose a smaller file.', 'error');
                  } else if (error.response.status === 401) {
                        this.showAlertMessage('Unauthorized. Please log in again.', 'error');
                    } else {
                        this.showAlertMessage(error.response.data.message || 'Error updating outfit. Please try again.', 'error');
                  }
                } else if (error.request) {
                    this.showAlertMessage('No response from server. Please try again later.', 'error');
                } else {
                    this.showAlertMessage('Error updating outfit. Please try again.', 'error');
                }
              } finally {
                this.isLoading = false;
              }
        },
        resetEditForm() {
          this.editingOutfit = {
            outfit_id: null,
            outfit_name: '',
            outfit_type: '',
            outfit_color: '',
            outfit_desc: '',
            rent_price: '',
            size: '',
            weight: '',
            status: 'Available'
          };
          this.editingOutfitArchive = {
            archive_id: null,
            outfit_id: null,
            creation_address: '',
            owner: ''
          };
          this.editingSelectedFile = null;
          this.editingSelectedFileName = null;
          this.errorMessage = '';
          this.isLoading = false;
          this.editImagePreview = null;
        },
        showAlertMessage(message, type = 'success') {
            this.alertMessage = message;
            this.alertType = type;
            this.showAlert = true;
            // Auto hide after 3 seconds
            setTimeout(() => {
                this.closeAlert();
            }, 3000);
        },

        closeAlert() {
            this.showAlert = false;
            this.alertMessage = '';
        },
    },
    
        mounted() {
            this.fetchGownPackages();
            this.fetchOutfits();
            this.fetchInactivePackages();
        },
    
    
    
    }
    
    
    </script>
    
    <style scoped>

    </style>