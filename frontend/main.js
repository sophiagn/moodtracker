
function getDateTime(){
    
    let now = new Date();

    // months are 0 indexed, therefore add 1 for correct month
    let dateString = now.getMonth() + 1 + "-" + now.getDate() + " " + now.getHours() + " " + + now.getMinutes();

    return dateString;

}

let currentDateTime = getDateTime();
console.log(currentDateTime);