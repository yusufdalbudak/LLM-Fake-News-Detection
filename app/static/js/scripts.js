// Add any JavaScript functionality if needed 

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#analysis-form');
    const textarea = document.querySelector('textarea');
    const loadingDiv = document.querySelector('#loading');
    const analyzeBtn = document.querySelector('#analyze-btn');
    const newArticleBtn = document.querySelector('#analyze-new-btn');
    const sampleArticleBtn = document.querySelector('#sample-article-btn');

    // Sample articles for demonstration
    const sampleArticles = [
        "Breaking: Scientists discover new renewable energy source that could revolutionize power generation. Researchers at MIT have developed a new type of solar cell that can convert sunlight into electricity with unprecedented efficiency...",
        "Local community comes together to rebuild historic landmark after natural disaster. Hundreds of volunteers worked tirelessly over the weekend to restore the 150-year-old community center...",
        "Tech company announces breakthrough in quantum computing research. The new quantum processor has demonstrated stability at room temperature, a major milestone in quantum computing development..."
    ];

    newArticleBtn.addEventListener('click', function() {
        // Clear the form and results
        textarea.value = '';
        const resultDiv = document.querySelector('.result');
        if (resultDiv) {
            resultDiv.style.display = 'none';
        }
        // Reset form state
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').textContent = 'Analyze Article';
        loadingDiv.style.display = 'none';
        
        // Reset textarea height
        textarea.style.height = '200px';
        textarea.focus();
        
        // Reset character counter
        updateCharacterCounter();
        
        // Clear any error messages
        clearErrors();
    });

    sampleArticleBtn.addEventListener('click', function() {
        const randomArticle = sampleArticles[Math.floor(Math.random() * sampleArticles.length)];
        textarea.value = randomArticle;
        
        // Reset form state
        const resultDiv = document.querySelector('.result');
        if (resultDiv) {
            resultDiv.style.display = 'none';
        }
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').textContent = 'Analyze Article';
        loadingDiv.style.display = 'none';
        
        // Update textarea height and character counter
        adjustTextareaHeight();
        updateCharacterCounter();
    });

    form.addEventListener('submit', function(e) {
        if (!textarea.value.trim()) {
            e.preventDefault();
            showError('Please enter some text to analyze');
            return;
        }

        // Show loading state
        loadingDiv.style.display = 'block';
        analyzeBtn.disabled = true;
        analyzeBtn.querySelector('.btn-text').textContent = 'Analyzing...';
        
        // Clear any previous errors
        clearErrors();
    });

    function adjustTextareaHeight() {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 500) + 'px'; // Max height of 500px
    }

    textarea.addEventListener('input', function() {
        adjustTextareaHeight();
        updateCharacterCounter();
    });

    function showError(message) {
        clearErrors(); // Clear any existing errors first
        const flashMessages = document.querySelector('.flash-messages') || createFlashMessagesContainer();
        const p = document.createElement('p');
        p.className = 'flash-message';
        p.textContent = message;
        flashMessages.appendChild(p);
    }

    function createFlashMessagesContainer() {
        const div = document.createElement('div');
        div.className = 'flash-messages';
        form.parentNode.insertBefore(div, form);
        return div;
    }

    function clearErrors() {
        const flashMessages = document.querySelector('.flash-messages');
        if (flashMessages) {
            flashMessages.innerHTML = '';
        }
    }

    const maxLength = 5000;
    textarea.maxLength = maxLength;
    
    const counterDiv = document.createElement('div');
    counterDiv.className = 'character-counter';
    textarea.parentNode.insertBefore(counterDiv, textarea.nextSibling);

    function updateCharacterCounter() {
        const remaining = maxLength - textarea.value.length;
        const percentage = (textarea.value.length / maxLength) * 100;
        
        counterDiv.textContent = `${remaining} characters remaining`;
        
        if (percentage > 90) {
            counterDiv.style.color = getComputedStyle(document.documentElement)
                .getPropertyValue('--danger-color').trim();
        } else if (percentage > 70) {
            counterDiv.style.color = '#f39c12';
        } else {
            counterDiv.style.color = getComputedStyle(document.documentElement)
                .getPropertyValue('--primary-color').trim();
        }
    }

    updateCharacterCounter();

    function scrollToResults() {
        const resultDiv = document.querySelector('.result');
        if (resultDiv) {
            setTimeout(() => {
                resultDiv.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'nearest'
                });
            }, 100); // Small delay to ensure content is rendered
        }
    }

    if (document.querySelector('.result')) {
        scrollToResults();
    }
}); 