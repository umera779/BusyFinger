const button = document.getElementById("mine-btn-js");

// Check if the button was previously disabled and handle it
window.onload = () => {
    const disabledTime = localStorage.getItem('disabledUntil');
    const currentTime = Date.now();
    if (disabledTime && currentTime < disabledTime) {
        // Button should be disabled
        disableButton(disabledTime - currentTime);
    }

    // Restore the button text from localStorage
    const storedButtonText = localStorage.getItem('buttonText');
    if (storedButtonText) {
        button.innerHTML = storedButtonText; // Restore the button text
    }

    // Restore the image source from localStorage


};

// Disable the button for a set period of time (e.g., 10 seconds)
button.addEventListener('click', function() {
    const disableDuration = 10000; // 10 seconds
    const originalText = button.innerHTML; // Store the original button text
    button.innerHTML = "typing"; // Change the text to "typing" when clicked
    localStorage.setItem('buttonText', "typing"); // Save the button text to localStorage
    


   
    // Step 1: First, update the counter via AJAX
    $('#counter-form').submit(function(e) {
        e.preventDefault(); // Prevent the default form submission
        $.ajax({
            url: $(this).attr('action'), // URL to send the request
            type: 'POST', // Use POST method
            data: $(this).serialize(), // Serialize the form data
            success: function(response) {
                // Update the counter value in the HTML
                $('#counter-value').text(response.counter_value);

                // Step 2: Now disable the button after the counter is updated
                localStorage.setItem('disabledUntil', Date.now() + disableDuration); // Save the time when the button will be enabled
                disableButton(disableDuration, originalText); // Disable the button
            },
            error: function(xhr, errmsg, err) {
                alert("There was an error with the request: " + errmsg);
            }
        });
    });
});

// Function to disable the button and revert the button text and image
function disableButton(duration, originalText) {
    button.disabled = true;
    button.classList.add('loading');
    setTimeout(function() {
        button.disabled = false;
        button.classList.remove('loading');
        button.innerHTML = originalText; // Reset the button text back to the original
        localStorage.setItem('buttonText', "Type"); // Save the original text to localStorage

      
 // Save the original image source to localStorage



    }, duration);
}
