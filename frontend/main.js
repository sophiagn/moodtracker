function openTab(tabName) {
    document.getElementById('content-frame').src = tabName + ".html";
}

document.getElementById("mainDropdown").addEventListener("change", function() {
    let selectedValue = this.value;
    let buttonContainers = [
        document.getElementById("buttonContainer1"),
        document.getElementById("buttonContainer2"),
        document.getElementById("buttonContainer3"),
        document.getElementById("buttonContainer4"),
        document.getElementById("buttonContainer5"),
        document.getElementById("buttonContainer6"),
        document.getElementById("buttonContainer7"),
        document.getElementById("buttonContainer8"),
        document.getElementById("buttonContainer9"),
        document.getElementById("buttonContainer10")
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
    } else if (selectedValue === "option5") {  
        buttonContainers[4].classList.remove("hidden"); 
    }  else if (selectedValue === "option6") {  
        buttonContainers[5].classList.remove("hidden"); 
    } else if (selectedValue === "option7") {  
        buttonContainers[6].classList.remove("hidden"); 
    } else if (selectedValue === "option8") {  
        buttonContainers[7].classList.remove("hidden"); 
    } else if (selectedValue === "option9") {  
        buttonContainers[8].classList.remove("hidden"); 
    } else if (selectedValue === "option10") {  
        buttonContainers[9].classList.remove("hidden"); 
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
    // form input validation, making sure user selected all options before saving data
    let category1 = document.getElementById("category").value;
    let emotion1 = document.getElementById("emotion").value;
    let intensity1 = document.getElementById("intensity").value;
    let reasons1 = document.getElementById("reasons").value;

    let statusMessage = document.querySelector("#statusMessage");

    if (!category1 || !emotion1 || !intensity1 || !reasons1) {
        statusMessage.textContent = "Please fill out all fields.";
        statusMessage.style.color = "red";
        statusMessage.style.display = "block"; // Show message
        return;
    }

    let moodEntry = {
        dayOfWeek: new Date().toLocaleString('en-us', { weekday: 'long'}),
        date: new Date().toISOString().split("T")[0], // YYYY-MM-DD
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true }),
        intensity: intensity1,
        emotion: emotion1,
        category: category1,
        reasons: reasons1.split(",") // Convert to list.
    };


    let moodJSON = JSON.stringify(moodEntry, null, 4);


    try {
        let response = await eel.saveToJson(moodJSON)();
        if(response === "Success"){
            statusMessage.textContent = "Successfully saved data!";
            statusMessage.style.color = "#2E8B57"
            statusMessage.style.display = "inline-block";

            //document.getElementById("intensity").value = "";
            //document.getElementById("reasons").value = "";
        } else {
            statusMessage.textContent = "Failed to save data.";
            statusMessage.style.display = "inline-block";
            statusMessage.style.color = "red";
        }
    } catch(error){
        console.log("There was an error sending the data to the backend:", error);
        statusMessage.textContent = "Failed to save data.";
        statusMessage.style.color = "red";
        statusMessage.style.display = "inline-block";
    }
}
    //highestDayFreq
    async function fetchMostFrequentEmotionDay(emotion) { 
        let result = await eel.highestFreqEmotionDay(emotion)(); 
        alert("Most frequent days: "+ result); 
    }

    //highestTimeFreq
    async function fetchMostFrequentEmotionTime(emotion) { 
        let result = await eel.highestFreqEmotionTime(emotion)(); 
        alert("Most frequent time: "+ result); 
        }
     
    //highestSeasonFreq    
    async function fetchMostFrequentEmotionSeason(emotion) {
        let result = await eel.highestFreqEmotionSeason(emotion)(); 
        alert("Most frequent season: "+ result); 
    }

    //IntensityOverall
    async function fetchIntensity() {
        let result = await eel.intensityOverall()(); 
        alert("Intensity Overall: "+ result +"/5"); 
    }

    //IntensityOverallDay
    async function fetchIntensityOverallDay(dayOfWeek){
        let result = await eel.intensityOverallDay(dayOfWeek)();
        alert("Intensity Overall on " + dayOfWeek + " is " + result +"/5");
    }

    //IntensityOverallTime
    async function fetchIntensityOverallTime(time) { 
        let result = await eel.intensityOverallTime(time)(); 
        alert("Intensity Overall at " +time+ ": " + result +"/5");     
    }

    //IntensityOverallSeason
    async function fetchIntensityOverallSeason(season) { 
        let result = await eel.intensityOverallSeason(season)(); 
        alert("Intensity Overall at " +season+ ": " + result +"/5");     
    }
    
    //IntensityByDay
    async function fetchIntensityByDay(emotion, dayOfWeek) { 
        let result = await eel.intensityByDay(emotion, dayOfWeek)(); 
        alert(emotion + "'s Overall Intensity" + " on " + dayOfWeek+ " is " + result +"/5");     
    }

    function submitIntensityByDay() {
        let emotion = document.getElementById("emotionDropdownDay").value;
        let dayOfWeek = document.getElementById("dayDropdown").value;
    
        if (!emotion || !dayOfWeek) {
            alert("Please select both an emotion and a day of the week.");
            return;
        }
    
        fetchIntensityByDay(emotion, dayOfWeek);
    }

    //IntensityByTime
    async function fetchIntensityByTime(emotion, time) { 
        let result = await eel.intensityByTime(emotion, time)(); 
        alert(emotion + "'s Overall Intensity" + " at " + time+ " is " + result +"/5");     
    }

    
    function submitIntensityByTime() {
        let emotion = document.getElementById("emotionDropdownTime").value;
        let time = document.getElementById("timeDropdown").value;

        if (!emotion || !time) {
            alert("Please select both an emotion and a time of day.");
            return;
        }
    
        fetchIntensityByTime(emotion, time);
    }
    

     //IntensityBySeason
     async function fetchIntensityBySeason(emotion, season) { 
        let result = await eel.intensityBySeason(emotion, season)(); 
        alert(emotion + "'s Overall Intensity" + " during " + season+ " is " + result +"/5");     
    }

    function submitIntensityBySeason() {
        let emotion = document.getElementById("emotionDropdownSeason").value;
        let season = document.getElementById("seasonDropdown").value;
    
        if (!emotion || !season) {
            alert("Please select both an emotion and a season.");
            return;
        }
    
        fetchIntensityBySeason(emotion, season);
    }