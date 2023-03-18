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


//To display gallery add photos form
function toggleFormDisplay() {
  const addForm = document.querySelector('.add-photos-form');
  if (addForm.style.display === 'block'){
    addForm.style.display = 'none'
  }else{
    addForm.style.display = 'block'
  }}



// To display weather info
  function toggleWeatherDisplay() {
    const weatherInfo = document.querySelector('.weather-info');
    if (weatherInfo.style.display === 'block'){
      weatherInfo.style.display = 'none'
    }else{
      weatherInfo.style.display = 'block'
    }}


    function confirmDelete(e){
      return confirm('Are you sure you want to delete?')
    }

    // Nav toggle
    function navToggle() {
      const primaryNav = document.querySelector('.primary-nav');
      const hamburgerIcon = document.querySelector('.mobile-nav-toggle')
      const visibility = primaryNav.getAttribute('data-visible') 
      if (visibility==='false'){
        primaryNav.setAttribute('data-visible', true)
        hamburgerIcon.setAttribute('data-icon-open', true)
      }else{
        primaryNav.setAttribute('data-visible', false)
        hamburgerIcon.setAttribute('data-icon-open', false)
      }
    }
    
