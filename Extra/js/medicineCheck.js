// Predefined medicines and quantities
const medicines = {
    "Aravadoc": 20,
    "Ibuprofen": 10,
    "Paracetamol": 15,
    "Zolpidem":22,
    "Zopiclone":11,
    "Ketoconazole":56,
    "Labetalol":99,
    "Lactulose":8,
    "Lamotrigine":65,
    "Lansoprazole":44,
    "Latanoprost":84,
    "Lercanidipine":22, 
    "Letrozole":0,
    "Levetiracetam":11,
    "Levothyroxine":1,
    "Lithium":1,
    
};

// Function to check medicine availability
function showMedicineAvailability() {
    const medicineName = document.getElementById('medName').value;
    const resultDiv = document.getElementById('result');

    if (medicines.hasOwnProperty(medicineName)) {
        resultDiv.innerHTML = `The medicine ${medicineName} is available with ${medicines[medicineName]} units.`;
    } else {
        resultDiv.innerHTML = `The medicine ${medicineName} is not available.`;
    }
}

// Attach the function to the search button
document.getElementById('searchButtonmed').addEventListener('click', showMedicineAvailability);