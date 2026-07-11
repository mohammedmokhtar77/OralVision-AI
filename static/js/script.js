document.addEventListener('DOMContentLoaded', () => {
    // 1. MOBILE RESPONSIVE NAVIGATION
    const burger = document.querySelector('.burger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (burger && navMenu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                burger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // 2. SCROLL INTERSECTION OBSERVER ANIMATIONS
    const scrollRevealElements = document.querySelectorAll('.scroll-reveal');
    
    if (scrollRevealElements.length > 0) {
        const revealCallback = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // Stop observing once animated
                    observer.unobserve(entry.target);
                }
            });
        };

        const revealObserver = new IntersectionObserver(revealCallback, {
            root: null,
            threshold: 0.15,
            rootMargin: '0px'
        });

        scrollRevealElements.forEach(element => {
            revealObserver.observe(element);
        });
    }

    // 3. DRAG & DROP FILE UPLOAD
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const uploadPrompt = document.getElementById('upload-prompt');
    const previewImg = document.getElementById('preview-img');
    const removeBtn = document.getElementById('remove-btn');
    const predictBtn = document.getElementById('predict-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const errorBanner = document.getElementById('error-banner');

    let selectedFile = null;

    if (dropZone && fileInput) {
        // Trigger file select click on drop-zone click
        dropZone.addEventListener('click', (e) => {
            // Prevent trigger recursion if clicking buttons inside the dropzone
            if (e.target.closest('#remove-btn') || e.target.closest('#predict-btn') || e.target.closest('input')) {
                return;
            }
            fileInput.click();
        });

        // Drag highlights
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
            }, false);
        });

        // Handle file drop
        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                processFile(files[0]);
            }
        });

        // Handle file select change
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                processFile(fileInput.files[0]);
            }
        });
    }

    function processFile(file) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        
        if (!allowedTypes.includes(file.type)) {
            showUploadError('Unsupported file type. Please upload a PNG, JPG, or JPEG image.');
            return;
        }

        selectedFile = file;
        hideUploadError();

        // Display image preview
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            uploadPrompt.style.display = 'none';
            previewContainer.style.display = 'flex';
        };
    }

    // Clear selected file
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            resetUploadForm();
        });
    }

    function resetUploadForm() {
        selectedFile = null;
        if (fileInput) fileInput.value = '';
        if (previewImg) previewImg.src = '';
        if (previewContainer) previewContainer.style.display = 'none';
        if (uploadPrompt) uploadPrompt.style.display = 'flex';
        hideUploadError();
    }

    // Submit prediction form via AJAX
    if (predictBtn) {
        predictBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!selectedFile) return;

            const formData = new FormData();
            formData.append('image', selectedFile);

            // Display loading overlay
            if (loadingOverlay) loadingOverlay.style.display = 'flex';

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(jsonErr => {
                        throw new Error(jsonErr.error || 'Server error occurred during prediction.');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success && data.redirect_url) {
                    // Redirect to results page
                    window.location.href = data.redirect_url;
                } else {
                    throw new Error('Invalid redirect payload received.');
                }
            })
            .catch(err => {
                // Hide loading spinner and output error message
                if (loadingOverlay) loadingOverlay.style.display = 'none';
                showUploadError(err.message || 'An error occurred during prediction.');
            });
        });
    }

    function showUploadError(msg) {
        if (errorBanner) {
            errorBanner.textContent = msg;
            errorBanner.style.display = 'block';
            errorBanner.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert(msg);
        }
    }

    function hideUploadError() {
        if (errorBanner) {
            errorBanner.style.display = 'none';
            errorBanner.textContent = '';
        }
    }

    // 4. ANIMATED CONFIDENCE PROGRESS BARS
    const barFills = document.querySelectorAll('.bar-fill');
    if (barFills.length > 0) {
        // Trigger width animation shortly after rendering to ensure transition fires
        setTimeout(() => {
            barFills.forEach(fill => {
                const targetPercentage = fill.getAttribute('data-percentage');
                fill.style.width = `${targetPercentage}%`;
            });
        }, 150);
    }
});
