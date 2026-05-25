document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.prevent-double-submit');

    forms.forEach((form) => {
        form.addEventListener('submit', function (event) {
            if (form.dataset.submitting === 'true') {
                event.preventDefault();
                event.stopImmediatePropagation();
                return false;
            }

            form.dataset.submitting = 'true';

            const buttons = form.querySelectorAll('button[type="submit"], input[type="submit"]');

            buttons.forEach((button) => {
                button.disabled = true;

                const loadingText = button.dataset.loadingText || 'Procesando...';

                if (button.tagName.toLowerCase() === 'button') {
                    button.innerText = loadingText;
                } else {
                    button.value = loadingText;
                }

                button.classList.add('opacity-70', 'cursor-not-allowed');
            });
        });
    });
});