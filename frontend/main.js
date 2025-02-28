function updateEmotions() {
    const category = document.querySelector(".mycategory");
    const emotionDropDown = document.querySelector(".emotion");

    // creating an emotions object
    const emotions = {
        "Good": ["Joyful", "Content", "Excited", "Loved", "Confident", "Graceful", "Proud", "Energetic"],
        "Neutral": ["Indifferent", "Bored", "Distant", "Calm"],
        "Bad": ["Stressed", "Angry", "Annoyed", "Disappointed", "Disgusted", "Embarrassed", "Sad", "Dreadful", "Anxious"]
    };

    //emotionDropDown.innerHTML = "<option value=''>Select an Emotion</option>";

    if(category in emotions){
        emotions[category].forEach(emotion => {
            let option = document.createElement("option");
            option.value = emotion;
            option.textContent = emotion;
            emotionDropDown.apppendChild(option);
        });
    }
}

async function saveMoodData(){
    let moodEntry = {
        dayOfWeek: new Date().toLocaleString('en-us', { weekday: 'long'}),
        date: new Date.toISOString().split("T")[0], // YYYY-MM-DD
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

    // try {
    //     await eel.save_to_json(moodJSON)();
    //     alert("Data saved successfully!");
    // } catch(error){
    //     console.error("Error sending data to backend:", error);
    //     alert("Failed to save data.");
    // }
}