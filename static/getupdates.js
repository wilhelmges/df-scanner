document.querySelectorAll('label input[type="file"]').forEach((input) => {
        const area = input.parentElement;

        ['dragenter', 'dragover'].forEach((eventName) => {
            area.addEventListener(eventName, (event) => {
                event.preventDefault();
                area.classList.add('border-primary');
            });
        });

        ['dragleave', 'drop'].forEach((eventName) => {
            area.addEventListener(eventName, (event) => {
                event.preventDefault();
                area.classList.remove('border-primary');
            });
        });

        area.addEventListener('drop', (event) => {
            if (event.dataTransfer.files.length) {
                input.files = event.dataTransfer.files;
            }
        });
    });