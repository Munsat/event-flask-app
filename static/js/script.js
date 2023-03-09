function searchFunc() {
  const searchInput = document.querySelector(".search-input");
  const allNames = document.querySelectorAll(".event-name");
  const eventContainer = document.querySelectorAll(".upcoming-events");
  const filterValue = searchInput.value.toLowerCase();

  for (i = 0; i < allNames.length; i++) {
    if (allNames[i].textContent.toLowerCase().indexOf(filterValue) > -1) {
      eventContainer[i].style.display = "";
    } else {
      eventContainer[i].style.display = "none";
    }
  }
};



const weatherLink = document.querySelector('.weather-link')
const weatherInfo = document.querySelector('.weather-info')

weatherLink.addEventListener('click', ()=>{
  if (weatherInfo.style.display === 'none'){
    weatherInfo.style.display = 'block'
  }else{
    weatherInfo.style.display = 'none'
  }
  
});