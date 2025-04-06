/**
 * Wolves Gaming - Perfil de Jugador JavaScript
 * Desarrollado por Claude - Versión 1.0.0
 */

document.addEventListener('DOMContentLoaded', function() {
    // Preloader
    window.addEventListener('load', function() {
        const preloader = document.querySelector('.wolves-preloader');
        if (preloader) {
            setTimeout(() => {
                preloader.style.opacity = '0';
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 300);
            }, 500);
        }
    });

    // Inicialización de componentes
    initializeCharts();
    initializeAlerts();
    setupAjaxRequests();
    setupTabNavigation();
    setupAvatarPreview();
    setupFilterHandlers();
    setupScrollEffects();

    // Tooltips y Popovers Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Manejar cambio de avatar
    setupAvatarUpload();
    
    // Manejar notificaciones
    setupNotifications();
    
    // Animar elementos
    animateElements();
});

/**
 * Configura los efectos de scroll
 */
function setupScrollEffects() {
    // Scroll suave para links de anclaje
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Obtener la altura de la barra de navegación
                const navHeight = document.querySelector('.wolves-profile-nav').offsetHeight;
                
                // Calcular la posición de desplazamiento
                const offsetTop = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight;
                
                // Scroll suave hasta la posición
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Actualizar URL sin recargar la página
                history.pushState(null, null, targetId);
                
                // Actualizar clase activa en la navegación
                document.querySelectorAll('.wolves-nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                document.querySelector(`.wolves-nav-link[href="${targetId}"]`).classList.add('active');
            }
        });
    });
    
    // Cambio de clase activa al hacer scroll
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.content-section');
        const navLinks = document.querySelectorAll('.wolves-nav-link');
        const navHeight = document.querySelector('.wolves-profile-nav').offsetHeight;
        
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navHeight - 50;
            const sectionHeight = section.offsetHeight;
            
            if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
                current = '#' + section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === current) {
                link.classList.add('active');
            }
        });
    });
}

/**
 * Inicializa gráficos de estadísticas
 */
function initializeCharts() {
    // Gráfico de habilidades
    const skillsChart = document.getElementById('skillsChart');
    if (skillsChart) {
        const ctx = skillsChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Precisión', 'Reflejos', 'Estrategia', 'Trabajo en Equipo', 'Concentración', 'Adaptabilidad'],
                datasets: [{
                    label: 'Habilidades',
                    data: [85, 70, 90, 75, 80, 65],
                    backgroundColor: 'rgba(69, 248, 130, 0.2)',
                    borderColor: '#45F882',
                    borderWidth: 2,
                    pointBackgroundColor: '#45F882',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#45F882'
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        pointLabels: {
                            color: 'rgba(255, 255, 255, 0.7)',
                            font: {
                                size: 12
                            }
                        },
                        ticks: {
                            display: false,
                            backdropColor: 'transparent'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    // Gráfico de victorias/derrotas
    const winLossChart = document.getElementById('winLossChart');
    if (winLossChart) {
        const ctx = winLossChart.getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Victorias', 'Derrotas', 'Empates'],
                datasets: [{
                    data: [65, 30, 5],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    borderColor: 'transparent',
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)',
                            padding: 20,
                            font: { size: 12 }
                        }
                    }
                },
                maintainAspectRatio: false
            }
        });
    }
    
    // Actualizar gráficos al cambiar filtros
    const statsGameFilter = document.getElementById('statsGameFilter');
    if (statsGameFilter) {
        statsGameFilter.addEventListener('change', function() {
            // Aquí iría el código AJAX para actualizar los datos
            // Por ahora simulamos un cambio en los datos
            setTimeout(() => {
                if (skillsChart) {
                    const newData = Array.from({length: 6}, () => Math.floor(Math.random() * 50) + 50);
                    skillsChart.data.datasets[0].data = newData;
                    skillsChart.update();
                }
                
                if (winLossChart) {
                    const newData = [
                        Math.floor(Math.random() * 50) + 50,
                        Math.floor(Math.random() * 30) + 20,
                        Math.floor(Math.random() * 15) + 5
                    ];
                    winLossChart.data.datasets[0].data = newData;
                    winLossChart.update();
                }
            }, 300);
        });
    }
}

/**
 * Inicializa alertas
 */
function initializeAlerts() {
    // Cerrar alertas
    document.querySelectorAll('.wolves-alert-close').forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.wolves-alert');
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
    
    // Auto-cerrar alertas después de un tiempo
    setTimeout(() => {
        document.querySelectorAll('.wolves-alert').forEach((alert, index) => {
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }, index * 200);
        });
    }, 5000);
}

/**
 * Configura navegación por pestañas
 */
function setupTabNavigation() {
    document.querySelectorAll('.wolves-nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover clase activa de todos los enlaces
            document.querySelectorAll('.wolves-nav-link').forEach(item => {
                item.classList.remove('active');
            });
            
            // Agregar clase activa al enlace seleccionado
            this.classList.add('active');
            
            // Actualizar la URL con el hash
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                history.pushState(null, null, targetId);
            }
        });
    });
}

/**
 * Configura vista previa de avatar
 */
function setupAvatarPreview() {
    const avatarFileInput = document.getElementById('avatarFile');
    if (avatarFileInput) {
        avatarFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('avatarPreview');
                    if (preview) {
                        preview.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

/**
 * Configura filtros
 */
function setupFilterHandlers() {
    // Filtros para partidas
    const matchGameFilter = document.getElementById('matchGameFilter');
    const matchResultFilter = document.getElementById('matchResultFilter');
    
    if (matchGameFilter && matchResultFilter) {
        const applyFilters = () => {
            const gameValue = matchGameFilter.value;
            const resultValue = matchResultFilter.value;
            
            // Aquí iría el código AJAX para filtrar partidas
            // Por ahora simulamos la filtración en el cliente
            const matchItems = document.querySelectorAll('.match-item');
            matchItems.forEach(item => {
                const gameId = item.getAttribute('data-game-id');
                const result = item.classList.contains('victoria') ? 'win' : 
                              item.classList.contains('derrota') ? 'loss' : 'draw';
                
                const showByGame = gameValue === 'all' || gameId === gameValue;
                const showByResult = resultValue === 'all' || result === resultValue;
                
                if (showByGame && showByResult) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        };
        
        matchGameFilter.addEventListener('change', applyFilters);
        matchResultFilter.addEventListener('change', applyFilters);
    }
}

/**
 * Configura peticiones AJAX
 */
function setupAjaxRequests() {
    // CSRF Token para peticiones AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    
    // Configuración global para AJAX
    function setupAjaxHeaders() {
        const headers = {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        };
        return headers;
    }
    
    // Mostrar notificación
    function showNotification(message, type = 'success') {
        const alertsContainer = document.querySelector('.wolves-alerts-container');
        if (!alertsContainer) {
            const newAlertsContainer = document.createElement('div');
            newAlertsContainer.className = 'wolves-alerts-container';
            document.body.appendChild(newAlertsContainer);
        }
        
        const alertHTML = `
            <div class="wolves-alert wolves-alert-${type}" style="opacity: 0; transform: translateX(100%);">
                <div class="wolves-alert-icon">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
                </div>
                <div class="wolves-alert-content">
                    <p>${message}</p>
                </div>
                <button type="button" class="wolves-alert-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        const alertsContainer2 = document.querySelector('.wolves-alerts-container');
        alertsContainer2.insertAdjacentHTML('beforeend', alertHTML);
        
        const newAlert = alertsContainer2.lastElementChild;
        
        // Animar entrada
        setTimeout(() => {
            newAlert.style.opacity = '1';
            newAlert.style.transform = 'translateX(0)';
        }, 10);
        
        // Configurar cierre
        newAlert.querySelector('.wolves-alert-close').addEventListener('click', function() {
            newAlert.style.opacity = '0';
            newAlert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                newAlert.remove();
            }, 300);
        });
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            if (newAlert && newAlert.parentNode) {
                newAlert.style.opacity = '0';
                newAlert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (newAlert && newAlert.parentNode) {
                        newAlert.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
    
    // Editar perfil
    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
            submitBtn.disabled = true;
            
            const formData = new FormData(this);
            
            fetch('/users/edit_profile/', {
                method: 'POST',
                body: formData,
                headers: setupAjaxHeaders()
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message || 'Perfil actualizado correctamente', 'success');
                    
                    // Actualizar datos en la página
                    if (data.nickname) {
                        document.querySelectorAll('.wolves-name').forEach(el => {
                            el.textContent = data.nickname;
                        });
                    }
                    
                    // Cerrar modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editProfileModal'));
                    if (modal) {
                        modal.hide();
                    }
                } else {
                    showNotification(data.message || 'Error al actualizar el perfil', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error del servidor. Inténtalo de nuevo más tarde.', 'error');
            })
            .finally(() => {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }
    
    // Cambiar avatar
    const changeAvatarForm = document.getElementById('changeAvatarForm');
    if (changeAvatarForm) {
        changeAvatarForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subiendo...';
            submitBtn.disabled = true;
            
            const formData = new FormData(this);
            
            fetch('/users/change_avatar/', {
                method: 'POST',
                body: formData,
                headers: setupAjaxHeaders()
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message || 'Avatar actualizado correctamente', 'success');
                    
                    // Actualizar avatar en la página
                    if (data.avatar_url) {
                        document.querySelectorAll('.wolves-avatar').forEach(el => {
                            el.src = data.avatar_url;
                        });
                    }
                    
                    // Cerrar modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('changeAvatarModal'));
                    if (modal) {
                        modal.hide();
                    }
                } else {
                    showNotification(data.message || 'Error al actualizar el avatar', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error del servidor. Inténtalo de nuevo más tarde.', 'error');
            })
            .finally(() => {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }
    
    // Añadir juego
    const addGameForm = document.getElementById('addGameForm');
    if (addGameForm) {
        addGameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Añadiendo...';
            submitBtn.disabled = true;
            
            const formData = new FormData(this);
            
            fetch('/users/add_game/', {
                method: 'POST',
                body: formData,
                headers: setupAjaxHeaders()
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message || 'Juego añadido correctamente', 'success');
                    
                    // Añadir juego a la lista en la página
                    if (data.game) {
                        const gamesList = document.querySelector('.user-games-list');
                        if (gamesList) {
                            const gameHTML = `
                                <div class="game-card" id="game-${data.game.id}">
                                    <div class="game-image">
                                        <img src="${data.game.image_url}" alt="${data.game.name}">
                                    </div>
                                    <div class="game-info">
                                        <h4>${data.game.name}</h4>
                                        <p>${data.game.platform}</p>
                                    </div>
                                    <div class="game-actions">
                                        <button type="button" class="wolves-btn wolves-btn-sm wolves-btn-danger delete-game-btn" data-game-id="${data.game.id}">
                                            <i class="fas fa-trash-alt"></i>
                                        </button>
                                    </div>
                                </div>
                            `;
                            gamesList.insertAdjacentHTML('beforeend', gameHTML);
                            
                            // Añadir evento para eliminar juego
                            const newDeleteBtn = document.querySelector(`#game-${data.game.id} .delete-game-btn`);
                            if (newDeleteBtn) {
                                setupDeleteGameButton(newDeleteBtn);
                            }
                        }
                    }
                    
                    // Limpiar formulario
                    this.reset();
                    
                    // Cerrar modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addGameModal'));
                    if (modal) {
                        modal.hide();
                    }
                } else {
                    showNotification(data.message || 'Error al añadir el juego', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error del servidor. Inténtalo de nuevo más tarde.', 'error');
            })
            .finally(() => {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }
    
    // Eliminar juego
    function setupDeleteGameButton(button) {
        button.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres eliminar este juego de tu perfil?')) {
                const gameId = this.getAttribute('data-game-id');
                const gameCard = document.getElementById(`game-${gameId}`);
                
                fetch(`/users/delete_game/${gameId}/`, {
                    method: 'POST',
                    headers: setupAjaxHeaders()
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message || 'Juego eliminado correctamente', 'success');
                        
                        // Eliminar juego de la página
                        if (gameCard) {
                            gameCard.style.opacity = '0';
                            gameCard.style.transform = 'scale(0.8)';
                            setTimeout(() => {
                                gameCard.remove();
                            }, 300);
                        }
                    } else {
                        showNotification(data.message || 'Error al eliminar el juego', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Error del servidor. Inténtalo de nuevo más tarde.', 'error');
                });
            }
        });
    }
    
    // Configurar botones existentes para eliminar juegos
    document.querySelectorAll('.delete-game-btn').forEach(button => {
        setupDeleteGameButton(button);
    });
    
    // Configurar solicitudes de amistad
    const sendFriendRequestBtn = document.getElementById('sendFriendRequest');
    if (sendFriendRequestBtn) {
        sendFriendRequestBtn.addEventListener('click', function() {
            const userId = this.getAttribute('data-user');
            const originalBtnText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            this.disabled = true;
            
            fetch('/users/send_friend_request/', {
                method: 'POST',
                body: JSON.stringify({
                    user_id: userId
                }),
                headers: {
                    ...setupAjaxHeaders(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message || 'Solicitud de amistad enviada correctamente', 'success');
                    
                    // Actualizar botón
                    this.innerHTML = '<i class="fas fa-check"></i> Solicitud Enviada';
                    this.disabled = true;
                    this.classList.remove('wolves-btn-primary');
                    this.classList.add('wolves-btn-secondary');
                } else {
                    showNotification(data.message || 'Error al enviar la solicitud de amistad', 'error');
                    this.innerHTML = originalBtnText;
                    this.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error del servidor. Inténtalo de nuevo más tarde.', 'error');
                this.innerHTML = originalBtnText;
                this.disabled = false;
            });
        });
    }
}

/**
 * Configurar la carga y previsualización de avatar
 */
function setupAvatarUpload() {
    const avatarFile = document.getElementById('avatarFile');
    const avatarPreview = document.getElementById('avatarPreview');
    const previewContainer = document.querySelector('.avatar-preview-container');
    
    if (avatarFile && avatarPreview) {
        avatarFile.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    previewContainer.classList.remove('d-none');
                }
                
                reader.readAsDataURL(file);
            } else {
                previewContainer.classList.add('d-none');
            }
        });
    }
    
    // Manejar el envío del formulario de avatar
    const avatarForm = document.getElementById('avatarForm');
    if (avatarForm) {
        avatarForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            // Mostrar estado de carga
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
            submitBtn.disabled = true;
            
            // Enviar datos con fetch API
            fetch('/usuario/actualizar_avatar/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mostrar mensaje de éxito
                    showNotification('Avatar actualizado correctamente', 'success');
                    
                    // Actualizar avatar en la página
                    const avatars = document.querySelectorAll('.wolves-avatar');
                    avatars.forEach(avatar => {
                        avatar.src = data.avatar_url;
                    });
                    
                    // Cerrar modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('avatarModal'));
                    modal.hide();
                    
                    // Resetear formulario
                    avatarForm.reset();
                    previewContainer.classList.add('d-none');
                } else {
                    // Mostrar mensaje de error
                    showNotification(data.error || 'Error al actualizar el avatar', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error al procesar la solicitud', 'error');
            })
            .finally(() => {
                // Restaurar estado del botón
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }
}

/**
 * Configurar el sistema de notificaciones
 */
function setupNotifications() {
    // Cerrar alertas al hacer clic en el botón de cerrar
    document.querySelectorAll('.close-alert').forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.wolves-alert');
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
}

/**
 * Animar elementos en la página
 */
function animateElements() {
    // Añadir clase para animar tarjetas
    const cards = document.querySelectorAll('.wolves-card');
    
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

/**
 * Inicializa tooltips
 */
function initializeTooltips() {
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Tooltips personalizados para los logros
    const achievements = document.querySelectorAll('.achievement-badge');
    
    achievements.forEach(badge => {
        const tooltipContent = badge.dataset.tooltip;
        if (!tooltipContent) return;
        
        badge.addEventListener('mouseenter', function(e) {
            createCustomTooltip(this, tooltipContent, e);
        });
        
        badge.addEventListener('mouseleave', function() {
            removeCustomTooltip();
        });
    });
}

/**
 * Crea un tooltip personalizado
 */
function createCustomTooltip(element, content, event) {
    // Eliminar tooltip existente
    removeCustomTooltip();
    
    // Crear nuevo tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'wolves-custom-tooltip';
    tooltip.innerHTML = content;
    document.body.appendChild(tooltip);
    
    // Posicionar tooltip
    const rect = element.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    tooltip.style.top = (rect.top - tooltipRect.height - 10) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltipRect.width / 2)) + 'px';
    
    // Animar entrada
    setTimeout(() => {
        tooltip.style.opacity = '1';
        tooltip.style.transform = 'translateY(0)';
    }, 10);
}

/**
 * Elimina el tooltip personalizado
 */
function removeCustomTooltip() {
    const tooltip = document.querySelector('.wolves-custom-tooltip');
    if (tooltip) {
        tooltip.style.opacity = '0';
        tooltip.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            tooltip.remove();
        }, 300);
    }
}

/**
 * Inicializa las tarjetas colapsables
 */
function initializeCollapsibleCards() {
    const cardHeaders = document.querySelectorAll('.card-header[data-collapsible="true"]');
    
    cardHeaders.forEach(header => {
        const cardId = header.closest('.wolves-card').id;
        const cardBody = header.nextElementSibling;
        const collapseIcon = document.createElement('i');
        collapseIcon.className = 'fas fa-chevron-up collapse-icon';
        
        header.appendChild(collapseIcon);
        
        header.addEventListener('click', function() {
            const isCollapsed = cardBody.classList.contains('collapsed');
            
            if (isCollapsed) {
                // Expandir
                cardBody.style.height = cardBody.scrollHeight + 'px';
                cardBody.classList.remove('collapsed');
                collapseIcon.className = 'fas fa-chevron-up collapse-icon';
                
                // Guardar estado
                localStorage.setItem('wolves_card_' + cardId, 'expanded');
                
                setTimeout(() => {
                    cardBody.style.height = '';
                }, 300);
            } else {
                // Colapsar
                cardBody.style.height = cardBody.scrollHeight + 'px';
                
                setTimeout(() => {
                    cardBody.style.height = '0';
                    collapseIcon.className = 'fas fa-chevron-down collapse-icon';
                    
                    // Guardar estado
                    localStorage.setItem('wolves_card_' + cardId, 'collapsed');
                }, 10);
                
                setTimeout(() => {
                    cardBody.classList.add('collapsed');
                }, 300);
            }
        });
        
        // Restaurar estado guardado
        if (cardId) {
            const savedState = localStorage.getItem('wolves_card_' + cardId);
            if (savedState === 'collapsed') {
                cardBody.classList.add('collapsed');
                cardBody.style.height = '0';
                collapseIcon.className = 'fas fa-chevron-down collapse-icon';
            }
        }
    });
}

/**
 * Configura los badges de logros
 */
function setupAchievementBadges() {
    const badges = document.querySelectorAll('.achievement-badge');
    
    badges.forEach(badge => {
        // Efecto hover
        badge.addEventListener('mouseenter', function() {
            this.classList.add('shine');
        });
        
        badge.addEventListener('mouseleave', function() {
            this.classList.remove('shine');
        });
        
        // Efecto click para mostrar detalles
        badge.addEventListener('click', function() {
            const achievementId = this.dataset.id;
            const achievementName = this.querySelector('.achievement-name').textContent;
            const achievementDesc = this.dataset.description || 'No hay descripción disponible';
            const achievementDate = this.dataset.date || 'Fecha desconocida';
            const achievementIcon = this.querySelector('i').className;
            
            showAchievementDetails(achievementId, achievementName, achievementDesc, achievementDate, achievementIcon);
        });
    });
}

/**
 * Muestra los detalles de un logro
 */
function showAchievementDetails(id, name, description, date, iconClass) {
    // Crear modal de detalles
    const modalHTML = `
    <div class="modal fade" id="achievementModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="${iconClass}"></i>
                        ${name}
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="achievement-detail-content">
                        <div class="achievement-icon-large">
                            <i class="${iconClass}"></i>
                        </div>
                        <div class="achievement-detail-text">
                            <p>${description}</p>
                            <div class="achievement-date">
                                <i class="fas fa-calendar-alt"></i>
                                <span>Conseguido: ${date}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Eliminar modal existente si hay uno
    const existingModal = document.getElementById('achievementModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Añadir modal al DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('achievementModal'));
    modal.show();
}

/**
 * Configura las tarjetas de estadísticas
 */
function setupStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
            
            // Mostrar información adicional si existe
            const extraInfo = this.dataset.extraInfo;
            if (extraInfo) {
                const infoContainer = document.createElement('div');
                infoContainer.className = 'stat-extra-info';
                infoContainer.innerHTML = extraInfo;
                
                this.appendChild(infoContainer);
                
                setTimeout(() => {
                    infoContainer.style.opacity = '1';
                    infoContainer.style.transform = 'translateY(0)';
                }, 10);
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
            
            // Ocultar información adicional
            const extraInfo = this.querySelector('.stat-extra-info');
            if (extraInfo) {
                extraInfo.style.opacity = '0';
                extraInfo.style.transform = 'translateY(10px)';
                
                setTimeout(() => {
                    extraInfo.remove();
                }, 300);
            }
        });
    });
}

/**
 * Efecto "float" para las redes sociales
 */
document.querySelectorAll('.social-icon').forEach(icon => {
    icon.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.1)';
    });
    
    icon.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1.0)';
    });
});

/**
 * Detección de streaming activo
 */
function checkStreamingStatus() {
    const twitchIcon = document.querySelector('.social-icon[data-platform="twitch"]');
    if (!twitchIcon) return;
    
    const twitchUsername = twitchIcon.dataset.username;
    if (!twitchUsername) return;
    
    // Consultar API de Twitch
    fetch(`/api/twitch/check_streaming/${twitchUsername}/`)
        .then(response => response.json())
        .then(data => {
            if (data.is_streaming) {
                twitchIcon.classList.add('streaming');
                twitchIcon.setAttribute('data-bs-original-title', '¡En vivo ahora!');
                
                // Actualizar tooltip si está inicializado
                const tooltip = bootstrap.Tooltip.getInstance(twitchIcon);
                if (tooltip) {
                    tooltip.update();
                }
            }
        })
        .catch(error => console.error('Error checking streaming status:', error));
}

// Llamar a checkStreamingStatus al cargar
checkStreamingStatus(); 