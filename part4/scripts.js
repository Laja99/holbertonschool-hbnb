const API_URL = 'http://127.0.0.1:5000/api/v1';

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function checkAuthentication() {
    const token = getCookie('token');
    
    if (window.location.pathname.includes('add_review.html') && !token) {
        window.location.href = 'index.html';
        return null;
    }

    const loginLink = document.querySelector('.login-button');
    const userDisplay = document.getElementById('user-name');

    if (token) {
        if (loginLink) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.onclick = (e) => {
                e.preventDefault();
                logoutUser();
            };
        }
        const userName = sessionStorage.getItem('userName');
        if (userName && userDisplay) {
            userDisplay.textContent = `Welcome, ${userName}`;
            userDisplay.style.display = 'inline';
        }
    }
    return token;
}

function logoutUser() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    sessionStorage.clear();
    window.location.reload();
}

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (response.ok) {
            return { success: true, token: data.access_token, userData: data };
        }
        return { success: false, error: data.error || data.msg || 'Login failed' };
    } catch (error) {
        return { success: false, error: 'Connection error' };
    }
}

async function fetchPlaces() {
    try {
        const response = await fetch(`${API_URL}/places/`);
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';
    places.forEach(place => {
        const article = document.createElement('article');
        article.className = 'place-card';
        article.setAttribute('data-price', place.price);
        article.innerHTML = `
            <div class="place-info">
                <h2>${place.title}</h2> 
                <p>Price per night: $${place.price}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        container.appendChild(article);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    const prices = ["All", "10", "50", "100"];
    filter.innerHTML = '';
    prices.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p;
        opt.textContent = p === "All" ? "All" : `Up to $${p}`;
        filter.appendChild(opt);
    });
    filter.addEventListener('change', (e) => {
        const maxPrice = e.target.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseFloat(card.getAttribute('data-price'));
            card.style.display = (maxPrice === "All" || price <= parseFloat(maxPrice)) ? 'flex' : 'none';
        });
    });
}

async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            displayReviews(place.reviews);
            if (document.getElementById('reviewing-title')) {
                document.getElementById('reviewing-title').textContent = `Reviewing: ${place.title}`;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;
    container.innerHTML = `
        <h1 class="details-title">${place.title}</h1>
        <div class="main-details-card">
            <p><strong>Host:</strong> ${place.host_name || 'Host'}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Amenities:</strong> ${place.amenities ? (Array.isArray(place.amenities) ? place.amenities.join(', ') : place.amenities) : 'WiFi, Pool, AC'}</p>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <a href="add_review.html?id=${place.id}" id="add-review-btn" class="details-button" style="background-color: #ff9800 !important;">Add a Review</a>
        </div>
    `;
}

function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    const currentUserId = sessionStorage.getItem('userId');
    const isAdmin = sessionStorage.getItem('isAdmin') === 'true';

    let html = '<h2 class="reviews-header">Reviews</h2>';
    if (!reviews || reviews.length === 0) {
        html += '<div class="review-card"><p>No reviews yet.</p></div>';
    } else {
        reviews.forEach(review => {
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            const canDelete = (String(review.user_id) === String(currentUserId) || isAdmin);
            html += `
                <div class="review-card">
                    <p><strong>${review.user_name}:</strong></p>
                    <p>${review.text || 'No review text'}</p> 
                    <p class="rating-stars">Rating: ${stars}</p>
                    
                    ${canDelete ? `
                        <button onclick="deleteReview('${review.id}')" class="delete-review-btn">
                            Delete Review
                        </button>
                    ` : ''}
                </div>
            `;
        });
    }
    reviewsSection.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const result = await loginUser(email, password);
            if (result.success) {
                setCookie('token', result.token, 7);
                const userId = result.userData.user_id || result.userData.id || (result.userData.user && result.userData.user.id);
                const isAdmin = result.userData.is_admin || (result.userData.user && result.userData.user.is_admin) || false;
                const firstName = result.userData.first_name || result.userData.full_name || email.split('@')[0];

                sessionStorage.setItem('userId', userId);
                sessionStorage.setItem('isAdmin', isAdmin);
                sessionStorage.setItem('userName', firstName);

                window.location.href = 'index.html';
            } else {
                const errorDiv = document.getElementById('error-message');
                if (errorDiv) {
                    errorDiv.textContent = result.error;
                    errorDiv.style.display = 'block';
                }
            }
        });
    }

    if (document.getElementById('places-list')) {
        fetchPlaces();
        setupPriceFilter();
    }

    if (placeId) {
        fetchPlaceDetails(placeId);
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm && token && placeId) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const comment = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            try {
                const response = await fetch(`${API_URL}/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        text: comment,
                        rating: parseInt(rating)
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const data = await response.json();
                    alert(`Error: ${data.error || 'Failed to submit'}`);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});

async function deleteReview(reviewId) {
    if (!confirm('Are you sure you want to delete this review?')) return;

    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to delete a review.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reviews/${reviewId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            alert('Review deleted successfully!');
            location.reload(); // إعادة تحميل الصفحة لتختفي المراجعة
        } else {
            const data = await response.json();
            alert(`Error: ${data.error || 'Failed to delete review'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while trying to delete the review.');
    }
}
