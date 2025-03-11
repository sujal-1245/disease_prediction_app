document.addEventListener("DOMContentLoaded", function () {
    const symptomDropdown = document.getElementById("symptoms");
    const addButton = document.getElementById("add-symptom");
    const symptomList = document.getElementById("symptom-list");
    const predictButton = document.getElementById("predict");
    const resultSection = document.getElementById("result");
    const diseaseName = document.getElementById("disease-name");
    const doctorList = document.getElementById("doctor-list");

    let selectedSymptoms = [];

    // Fetch symptoms for dropdown
    fetch("/get_symptoms")
        .then(response => response.json())
        .then(symptoms => {
            symptoms.forEach(symptom => {
                let option = document.createElement("option");
                option.value = symptom;
                option.textContent = symptom;
                symptomDropdown.appendChild(option);
            });
        });

    // Add symptom to list
    addButton.addEventListener("click", function () {
        let selected = symptomDropdown.value;
        if (selected && !selectedSymptoms.includes(selected)) {
            selectedSymptoms.push(selected);
            let listItem = document.createElement("li");
            listItem.textContent = selected;
            symptomList.appendChild(listItem);
        }
    });

    // Predict Disease
    predictButton.addEventListener("click", function () {
        fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symptoms: selectedSymptoms })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                resultSection.classList.remove("hidden");
                diseaseName.textContent = data.disease;

                doctorList.innerHTML = "";
                data.doctors.forEach(doc => {
                    let item = document.createElement("li");
                    item.textContent = `${doc.name}, ${doc.specialization}, ${doc.hospital} (${doc.location})`;
                    doctorList.appendChild(item);
                });
            }
        });
    });
});
