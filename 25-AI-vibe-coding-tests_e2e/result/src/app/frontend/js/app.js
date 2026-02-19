/**
 * Simple Web Blog - Frontend Application
 * JavaScript for handling UI interactions and API calls
 */

// ============================================================================
// Configuration
// ============================================================================

const API_BASE_URL = 'http://localhost:5000/api';

// ============================================================================
// State Management
// ============================================================================

let currentSection = 'posts';
let users = [];
let posts = [];

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    loadPosts();
    loadUsers();
});

// ============================================================================
// Navigation
// ============================================================================

function showSection(section) {
    // Update navigation
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
        if (link.textContent.toLowerCase().includes(section)) {
            link.classList.add('active');
        }
    });

    // Hide all sections
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
        sec.classList.add('hidden');
    });

    // Show selected section
    const selectedSection = document.getElementById(`${section}-section`);
    if (selectedSection) {
        selectedSection.classList.remove('hidden');
        selectedSection.classList.add('active');
    }

    currentSection = section;

    // Load data for the section
    switch (section) {
        case 'posts':
            loadPosts();
            break;
        case 'users':
            loadUsers();
            break;
        case 'stats':
            loadStats();
            break;
    }
}

// ============================================================================
// API Calls - Posts
// ============================================================================

async function loadPosts() {
    const container = document.getElementById('posts-list');
    container.innerHTML = '<div class="loading">Loading posts</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/posts`);
        if (!response.ok) throw new Error('Failed to load posts');
        
        posts = await response.json();
        renderPosts(posts);
    } catch (error) {
        console.error('Error loading posts:', error);
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">⚠️</div>
                <p>Unable to load posts. Make sure the backend server is running.</p>
            </div>
        `;
    }
}

async function createPost(title, content, userId) {
    const response = await fetch(`${API_BASE_URL}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, user_id: userId })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create post');
    }

    return response.json();
}

async function updatePost(postId, title, content) {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to update post');
    }

    return response.json();
}

async function deletePost(postId) {
    if (!confirm('Are you sure you want to delete this post?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete post');

        showToast('Post deleted successfully', 'success');
        loadPosts();
    } catch (error) {
        console.error('Error deleting post:', error);
        showToast('Failed to delete post', 'error');
    }
}

// ============================================================================
// API Calls - Users
// ============================================================================

async function loadUsers() {
    const container = document.getElementById('users-list');
    container.innerHTML = '<div class="loading">Loading users</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        if (!response.ok) throw new Error('Failed to load users');
        
        users = await response.json();
        renderUsers(users);
        updateAuthorSelect();
    } catch (error) {
        console.error('Error loading users:', error);
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">⚠️</div>
                <p>Unable to load users. Make sure the backend server is running.</p>
            </div>
        `;
    }
}

async function createUser(username, email) {
    const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create user');
    }

    return response.json();
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? All their posts will also be deleted.')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete user');

        showToast('User deleted successfully', 'success');
        loadUsers();
        loadPosts(); // Refresh posts as they may have been deleted
    } catch (error) {
        console.error('Error deleting user:', error);
        showToast('Failed to delete user', 'error');
    }
}

// ============================================================================
// API Calls - Statistics
// ============================================================================

async function loadStats() {
    const container = document.getElementById('stats-container');
    container.innerHTML = '<div class="loading">Loading statistics</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (!response.ok) throw new Error('Failed to load statistics');
        
        const stats = await response.json();
        renderStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">📊</div>
                <p>Unable to load statistics. Make sure the backend server is running.</p>
            </div>
        `;
    }
}

// ============================================================================
// Rendering Functions
// ============================================================================

function renderPosts(posts) {
    const container = document.getElementById('posts-list');

    if (posts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">📝</div>
                <p>No posts yet. Create your first post!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = posts.map(post => `
        <div class="card">
            <div class="card-header">
                <h3 class="card-title" onclick="showPostDetail(${post.id})">${escapeHtml(post.title)}</h3>
            </div>
            <div class="card-meta">
                By ${escapeHtml(post.author || 'Unknown')} • ${formatDate(post.created_at)}
                ${post.updated_at !== post.created_at ? `<br>Updated: ${formatDate(post.updated_at)}` : ''}
            </div>
            <div class="card-content">
                ${escapeHtml(truncateText(post.content, 150))}
            </div>
            <div class="card-actions">
                <button class="btn btn-secondary btn-small" onclick="showPostDetail(${post.id})">View</button>
                <button class="btn btn-primary btn-small" onclick="editPost(${post.id})">Edit</button>
                <button class="btn btn-danger btn-small" onclick="deletePost(${post.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function renderUsers(users) {
    const container = document.getElementById('users-list');

    if (users.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">👤</div>
                <p>No users yet. Create your first user!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = users.map(user => `
        <div class="card">
            <div class="card-header">
                <h3 class="card-title" onclick="showUserDetail(${user.id})">${escapeHtml(user.username)}</h3>
            </div>
            <div class="card-meta">
                ${escapeHtml(user.email)}
            </div>
            <div class="card-content">
                <strong>${user.post_count}</strong> post${user.post_count !== 1 ? 's' : ''}<br>
                Joined: ${formatDate(user.created_at)}
            </div>
            <div class="card-actions">
                <button class="btn btn-secondary btn-small" onclick="showUserDetail(${user.id})">View</button>
                <button class="btn btn-danger btn-small" onclick="deleteUser(${user.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function renderStats(stats) {
    const container = document.getElementById('stats-container');

    container.innerHTML = `
        <div class="stat-card highlight">
            <div class="stat-value">${stats.total_users}</div>
            <div class="stat-label">Total Users</div>
        </div>
        <div class="stat-card highlight">
            <div class="stat-value">${stats.total_posts}</div>
            <div class="stat-label">Total Posts</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.most_active_user ? stats.most_active_user.post_count : 0}</div>
            <div class="stat-label">Most Active: ${stats.most_active_user ? escapeHtml(stats.most_active_user.username) : 'N/A'}</div>
        </div>
        <div class="stat-list">
            <h4>📊 Posts per User</h4>
            <ul>
                ${stats.posts_per_user.length > 0 ? 
                    stats.posts_per_user.map(u => `
                        <li>
                            <span>${escapeHtml(u.username)}</span>
                            <span><strong>${u.post_count}</strong> posts</span>
                        </li>
                    `).join('') : 
                    '<li>No users yet</li>'
                }
            </ul>
        </div>
        <div class="stat-list">
            <h4>📰 Recent Posts</h4>
            <ul>
                ${stats.recent_posts.length > 0 ? 
                    stats.recent_posts.map(p => `
                        <li>
                            <span>${escapeHtml(p.title)}</span>
                            <span>by ${escapeHtml(p.author)}</span>
                        </li>
                    `).join('') : 
                    '<li>No posts yet</li>'
                }
            </ul>
        </div>
    `;
}

// ============================================================================
// Modal Functions - Posts
// ============================================================================

function showPostForm() {
    document.getElementById('post-form-title').textContent = 'Create New Post';
    document.getElementById('post-form').reset();
    document.getElementById('post-id').value = '';
    updateAuthorSelect();
    document.getElementById('post-form-modal').classList.remove('hidden');
}

function hidePostForm() {
    document.getElementById('post-form-modal').classList.add('hidden');
}

async function savePost(event) {
    event.preventDefault();

    const postId = document.getElementById('post-id').value;
    const title = document.getElementById('post-title-input').value;
    const content = document.getElementById('post-content-input').value;
    const userId = document.getElementById('post-author-select').value;

    try {
        if (postId) {
            // Update existing post
            await updatePost(postId, title, content);
            showToast('Post updated successfully', 'success');
        } else {
            // Create new post
            await createPost(title, content, userId);
            showToast('Post created successfully', 'success');
        }

        hidePostForm();
        loadPosts();
    } catch (error) {
        console.error('Error saving post:', error);
        showToast(error.message, 'error');
    }
}

function editPost(postId) {
    const post = posts.find(p => p.id === postId);
    if (!post) return;

    document.getElementById('post-form-title').textContent = 'Edit Post';
    document.getElementById('post-id').value = post.id;
    document.getElementById('post-title-input').value = post.title;
    document.getElementById('post-content-input').value = post.content;
    updateAuthorSelect();
    document.getElementById('post-author-select').value = post.user_id;
    document.getElementById('post-author-select').disabled = true; // Can't change author

    document.getElementById('post-form-modal').classList.remove('hidden');
}

async function showPostDetail(postId) {
    try {
        const response = await fetch(`${API_BASE_URL}/posts/${postId}`);
        if (!response.ok) throw new Error('Failed to load post');
        
        const post = await response.json();
        
        document.getElementById('post-detail-content').innerHTML = `
            <div class="post-detail">
                <h2>${escapeHtml(post.title)}</h2>
                <div class="meta">
                    By <strong>${escapeHtml(post.author || 'Unknown')}</strong><br>
                    Created: ${formatDate(post.created_at)}
                    ${post.updated_at !== post.created_at ? `<br>Updated: ${formatDate(post.updated_at)}` : ''}
                </div>
                <div class="content">${escapeHtml(post.content)}</div>
            </div>
        `;
        
        document.getElementById('post-detail-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading post detail:', error);
        showToast('Failed to load post details', 'error');
    }
}

function hidePostDetail() {
    document.getElementById('post-detail-modal').classList.add('hidden');
}

// ============================================================================
// Modal Functions - Users
// ============================================================================

function showUserForm() {
    document.getElementById('user-form').reset();
    document.getElementById('user-form-modal').classList.remove('hidden');
}

function hideUserForm() {
    document.getElementById('user-form-modal').classList.add('hidden');
}

async function saveUser(event) {
    event.preventDefault();

    const username = document.getElementById('username-input').value;
    const email = document.getElementById('email-input').value;

    try {
        await createUser(username, email);
        showToast('User created successfully', 'success');
        hideUserForm();
        loadUsers();
    } catch (error) {
        console.error('Error creating user:', error);
        showToast(error.message, 'error');
    }
}

async function showUserDetail(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`);
        if (!response.ok) throw new Error('Failed to load user');
        
        const user = await response.json();
        
        document.getElementById('user-detail-content').innerHTML = `
            <div class="user-detail">
                <h2>👤 ${escapeHtml(user.username)}</h2>
                <div class="info">
                    <p><span class="label">Email:</span> ${escapeHtml(user.email)}</p>
                    <p><span class="label">Posts:</span> ${user.post_count}</p>
                    <p><span class="label">Member since:</span> ${formatDate(user.created_at)}</p>
                </div>
            </div>
        `;
        
        document.getElementById('user-detail-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading user detail:', error);
        showToast('Failed to load user details', 'error');
    }
}

function hideUserDetail() {
    document.getElementById('user-detail-modal').classList.add('hidden');
}

// ============================================================================
// Helper Functions
// ============================================================================

function updateAuthorSelect() {
    const select = document.getElementById('post-author-select');
    select.disabled = false;
    select.innerHTML = '<option value="">Select an author</option>' +
        users.map(user => `<option value="${user.id}">${escapeHtml(user.username)}</option>`).join('');
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ============================================================================
// Toast Notifications
// ============================================================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
