
const themeToggle = document.querySelector('#theme-toggle');

// LISTEN for a click.
themeToggle.addEventListener('click', () => {
    // CHANGE: add the 'dark' class if missing, remove it if present.
    // CSS then re-reads every var(--surface), var(--text), etc.
    document.body.classList.toggle('dark');

    // Swap the icon to match the current mode.
    const isDark = document.body.classList.contains('dark');
    themeToggle.textContent = isDark ? '\u2600\uFE0F' : '\uD83C\uDF19'; // ☀️ or 🌙
});

/* ---------- 2. BACK-TO-TOP BUTTON ---------- */

// FIND the button.
const toTop = document.querySelector('#to-top');

// LISTEN for scrolling on the whole window.
window.addEventListener('scroll', () => {
    // CHANGE: show the button only after scrolling down 300px.
    if (window.scrollY > 300) {
        toTop.classList.add('show');
    } else {
        toTop.classList.remove('show');
    }
});

// LISTEN for a click on the button itself.
toTop.addEventListener('click', () => {
    // CHANGE: scroll smoothly back to the top of the page.
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ---------- 3. SCROLL REVEAL ---------- */

// FIND every element that has the class "reveal".
const revealItems = document.querySelectorAll('.reveal');

// IntersectionObserver watches elements and tells us when
// they enter the screen. It is far smoother than the scroll event.
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        // When an element scrolls into view...
        if (entry.isIntersecting) {
            // CHANGE: add the class that fades + slides it in.
            entry.target.classList.add('is-visible');
            // Stop watching it - it only needs to animate once.
            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.15 // fire when 15% of the element is visible
});

// Tell the observer to watch each reveal element.
revealItems.forEach((item) => observer.observe(item));

const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.projects-grid .card');
const currentCountEl = document.getElementById('current-count');
const totalCountEl = document.getElementById('total-count');

// Initialize total count baseline text if elements exist on page.
if (totalCountEl && projectCards.length > 0) {
    totalCountEl.textContent = projectCards.length;
}

// FUNCTION to manage visibility states.
function updateGallery(filterValue) {
    let visibleCount = 0;

    projectCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');

        // CHANGE: Show if it matches category or if 'all' is chosen.
        if (filterValue === 'all' || cardCategory === filterValue) {
            card.classList.remove('is-hidden');
            visibleCount++;
        } else {
            card.classList.add('is-hidden');
        }
    });

    // CHANGE: Dynamic numerical string injection for current items.
    if (currentCountEl) {
        currentCountEl.textContent = visibleCount;
    }
}

// LISTEN for clicks on each filter button.
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // SWAP active class state on buttons.
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // RUN gallery filter logic update.
        const targetFilter = button.getAttribute('data-filter');
        updateGallery(targetFilter);
    });
});

// Initialize on page load
if (filterButtons.length > 0) {
    updateGallery('all');
}