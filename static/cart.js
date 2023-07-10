var modal = document.getElementById("modal");
    var openModalBtn = document.getElementById("openModal");
    var closeButton = document.getElementsByClassName("close")[0];
    var backBtn = document.getElementById("backButton");
    var confirmBtn = document.getElementById("confirmButton");

    openModalBtn.onclick = function() {
      modal.style.display = "block";
    };

    closeButton.onclick = function() {
      modal.style.display = "none";
    };

    backBtn.onclick = function() {
      modal.style.display = "none";
    };

    confirmBtn.onclick = function() {
      // Add your logic for confirming the modal action
      modal.style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };

    $(document).ready(function() {
    $('.close-modal-btn').click(function() {
      // Hide the modal when the close button is clicked
      $('#modal').hide();
    });
  });