function openTab(tabName) {
    document.getElementById('content-frame').src = tabName + ".html";
}

document.getElementById("mainDropdown").addEventListener("change", function() {
    let selectedValue = this.value;
    let buttonContainers = [
        document.getElementById("buttonContainer1"),
        document.getElementById("buttonContainer2"),
        document.getElementById("buttonContainer3"),
        document.getElementById("buttonContainer4")
    ];

    // Hide all containers initially
    buttonContainers.forEach(container => container.classList.add("hidden"));

    // Show specific container based on selection
    if (selectedValue === "option1") {
        buttonContainers[0].classList.remove("hidden");
    } else if (selectedValue === "option2") {
        buttonContainers[1].classList.remove("hidden");
    } else if (selectedValue === "option3") {
        buttonContainers[2].classList.remove("hidden");
    } else if (selectedValue === "option4") {
        buttonContainers[3].classList.remove("hidden");
    }
});

function updateEmotions() {
    const category = document.getElementById("category").value;
    const emotionDropdown = document.getElementById("emotion");
   
    const emotions = {
        "Good": ["Joyful", "Content", "Excited", "Loved", "Confident", "Grateful", "Proud", "Energetic"],
        "Neutral": ["Indifferent", "Bored", "Distant", "Calm"],
        "Bad": ["Stressed", "Angry", "Annoyed", "Disappointed", "Disgusted", "Embarrassed", "Sad", "Dreadful", "Anxious"]
    };
   
    emotionDropdown.innerHTML = "<option value=''>Select an Emotion</option>";
   
    if (category in emotions) {
        emotions[category].forEach(emotion => {
            let option = document.createElement("option");
            option.value = emotion;
            option.textContent = emotion;
            emotionDropdown.appendChild(option);
        });
    }
}


async function saveMoodData(){
    let moodEntry = {
        dayOfWeek: new Date().toLocaleString('en-us', { weekday: 'long'}),
        date: new Date().toISOString().split("T")[0], // YYYY-MM-DD
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
        intensity: document.getElementById("intensity").value,
        emotion: document.getElementById("emotion").value,
        category: document.getElementById("category").value,
        reasons: document.getElementById("reasons").value.split(",") // Convert to list.
    };


    let moodJSON = JSON.stringify(moodEntry, null, 4);


    try {
        let response = await eel.saveToJson(moodJSON)();
        if(response === "Success"){
            alert("Data saved successfully!");
        } else {
            alert("Failed to save data.")
        }
    } catch(error){
        console.log("There was an error sending the data to the backend:", error);
        alert("Failed to save data.")
    }
}

 async function fetchMostFrequentEmotionDay(emotion) { 
    alert("Most frequent days:", emotion);
    let result = await eel.highestFreqEmotionDay(emotion)(); alert("Most frequent days:", result); 
    }

function getDateTime(){
    
    let now = new Date();

    // months are 0 indexed, therefore add 1 for correct month
    let dateString = now.getMonth() + 1 + "-" + now.getDate() + " " + now.getHours() + " " + + now.getMinutes();

    return dateString;

}

let currentDateTime = getDateTime();
console.log(currentDateTime);

