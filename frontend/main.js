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
    //highestDayFreq
    async function fetchMostFrequentEmotionDay(emotion) { 
        let result = await eel.highestFreqEmotionDay(emotion)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay1");
        let displayElement2 = document.getElementById("emotionResultDisplay2");
        let resultContainer = document.getElementById("result1");

        //alert("Most frequent days: "+ result); 
        displayElement1.textContent = `What day of the week am I most likely to feel ${emotion}?`;
        displayElement2.textContent = "\n"+ result;

        resultContainer.classList.remove("hidden");


    }

    //highestTimeFreq
    async function fetchMostFrequentEmotionTime(emotion) { 
        let result = await eel.highestFreqEmotionTime(emotion)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay3");
        let displayElement2 = document.getElementById("emotionResultDisplay4");
        let resultContainer = document.getElementById("result2");

        displayElement1.textContent = `What time of day am I most likely to feel ${emotion}?`;
        displayElement2.textContent = "\n"+ result;

        resultContainer.classList.remove("hidden");

        }
     
    //highestSeasonFreq    
    async function fetchMostFrequentEmotionSeason(emotion) {
        let result = await eel.highestFreqEmotionSeason(emotion)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay5");
        let displayElement2 = document.getElementById("emotionResultDisplay6");
        let resultContainer = document.getElementById("result3");

        displayElement1.textContent = `What time of year am I most likely to feel ${emotion}?`;
        displayElement2.textContent = "\n"+ result;

        resultContainer.classList.remove("hidden");
   
    }

    //IntensityOverall
    async function fetchIntensity() {
        let result = await eel.intensityOverall()(); 
        let displayElement1 = document.getElementById("emotionResultDisplay7");
        let displayElement2 = document.getElementById("emotionResultDisplay8");
        let resultContainer = document.getElementById("result4");

        displayElement1.textContent = `How intensely do I feel my emotions overall?`;
        displayElement2.textContent = "\n"+ result + "/5";

        resultContainer.classList.remove("hidden");
 
    }

    //IntensityOverallDay
    async function fetchIntensityOverallDay(dayOfWeek){
        let result = await eel.intensityOverallDay(dayOfWeek)();
        let displayElement1 = document.getElementById("emotionResultDisplay9");
        let displayElement2 = document.getElementById("emotionResultDisplay10");
        let resultContainer = document.getElementById("result5");

        displayElement1.textContent = `How intensely do I feel my emotions overall on a ${dayOfWeek}?`;
        displayElement2.textContent = "Intensity overall on " + dayOfWeek + " is " + result + "/5";

        resultContainer.classList.remove("hidden");
    }

    //IntensityOverallTime
    async function fetchIntensityOverallTime(time) { 
        let result = await eel.intensityOverallTime(time)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay11");
        let displayElement2 = document.getElementById("emotionResultDisplay12");
        let resultContainer = document.getElementById("result6");

        displayElement1.textContent = `How intensely do I feel my emotions overall during the ${time}?`;
        displayElement2.textContent = "Intensity overall at " + time + " is " + result + "/5";

        resultContainer.classList.remove("hidden"); 
    }

    //IntensityOverallSeason
    async function fetchIntensityOverallSeason(season) { 
        let result = await eel.intensityOverallSeason(season)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay13");
        let displayElement2 = document.getElementById("emotionResultDisplay14");
        let resultContainer = document.getElementById("result7");

        displayElement1.textContent = `How intensely do I feel my emotions overall during the ${season}?`;
        displayElement2.textContent = "Intensity overall at " + season + " is " + result + "/5";

        resultContainer.classList.remove("hidden"); 

    }
    
    //IntensityByDay
    async function fetchIntensityByDay(emotion, dayOfWeek) { 
        let result = await eel.intensityByDay(emotion, dayOfWeek)(); 
        let displayElement1 = document.getElementById("emotionResultDisplay15");
        let displayElement2 = document.getElementById("emotionResultDisplay16");
        let resultContainer = document.getElementById("result8");

        displayElement1.textContent = `How intensely do I feel ${emotion} on a ${dayOfWeek}?`;
        displayElement2.textContent = "Overall intensity of " + emotion + " on a " + dayOfWeek + " is " + result +"/5";

        resultContainer.classList.remove("hidden"); 
  
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
        let displayElement1 = document.getElementById("emotionResultDisplay17");
        let displayElement2 = document.getElementById("emotionResultDisplay18");
        let resultContainer = document.getElementById("result9");

        displayElement1.textContent = `How intensely do I feel ${emotion} during the ${time}?`;
        displayElement2.textContent = "Overall intensity of " + emotion + " during the " + time + " is " + result +"/5";

        resultContainer.classList.remove("hidden");  
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
        let displayElement1 = document.getElementById("emotionResultDisplay19");
        let displayElement2 = document.getElementById("emotionResultDisplay20");
        let resultContainer = document.getElementById("result10");

        displayElement1.textContent = `How intensely do I feel ${emotion} during ${season}?`;
        displayElement2.textContent = "Overall intensity of " + emotion + " during " + season + " is " + result +"/5";

        resultContainer.classList.remove("hidden"); 
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