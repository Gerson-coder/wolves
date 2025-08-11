/**
 * Modelo Conceptual SIGTI - Script Interactivo
 * 
 * Este script proporciona funcionalidades interactivas para el modelo conceptual
 * de la base de datos SIGTI, incluyendo:
 * - Destacar relaciones entre entidades
 * - Animaciones de transición
 * - Funcionalidades de zoom y desplazamiento
 * - Visualización dinámica de flujos de trabajo
 */

document.addEventListener('DOMContentLoaded', function() {
    // ----- Variables globales -----
    let scale = 1;
    const modelContent = document.querySelector('.model-content');
    const zoomStep = 0.1;
    let highlightRelationships = false;
    let dragActive = false;
    let startX, startY, scrollLeft, scrollTop;
    let entityRelations = {};
    
    // ----- Inicialización -----
    initializeRelations();
    setupEventListeners();
    animateEntrance();
    
    // ----- Funciones principales -----
    
    /**
     * Inicializa el mapeo de relaciones entre entidades
     */
    function initializeRelations() {
        // Mapeo de relaciones entre entidades para destacar conexiones
        entityRelations = {
            'entity-usuario': ['entity-sar', 'entity-ticket', 'entity-notificacion'],
            'entity-sar': ['entity-usuario', 'entity-ticket', 'entity-documento'],
            'entity-ticket': ['entity-sar', 'entity-usuario', 'entity-solucion', 'entity-sla', 'entity-auditoria'],
            'entity-solucion': ['entity-ticket'],
            'entity-documento': ['entity-sar'],
            'entity-notificacion': ['entity-usuario'],
            'entity-auditoria': ['entity-ticket'],
            'entity-sla': ['entity-ticket']
        };
    }
    
    /**
     * Configura todos los event listeners
     */
    function setupEventListeners() {
        // Controles de zoom
        document.getElementById('zoomIn').addEventListener('click', zoomIn);
        document.getElementById('zoomOut').addEventListener('click', zoomOut);
        document.getElementById('resetZoom').addEventListener('click', resetZoom);
        
        // Destacar relaciones
        document.getElementById('toggleRelationships').addEventListener('click', toggleRelationshipHighlight);
        
        // Exportar imagen
        document.getElementById('exportImage').addEventListener('click', exportModelAsImage);
        
        // Eventos interactivos para entidades
        setupEntityInteractions();
        
        // Eventos de arrastrar para desplazamiento
        setupDragScrolling();
        
        // Eventos de rueda del ratón para zoom
        setupWheelZoom();
    }
    
    /**
     * Configura interacciones para las entidades (click, hover, etc.)
     */
    function setupEntityInteractions() {
        const entityCards = document.querySelectorAll('.entity');
        
        entityCards.forEach(entity => {
            // Destacar al hacer clic
            entity.addEventListener('click', function() {
                highlightRelatedEntities(entity.id);
            });
            
            // Mostrar info al pasar el ratón por encima
            entity.addEventListener('mouseenter', function() {
                showEntityTooltip(entity.id);
            });
            
            entity.addEventListener('mouseleave', function() {
                hideEntityTooltip();
            });
            
            // Añadir clase para efectos CSS
            entity.classList.add('entity-highlight-effect');
        });
    }
    
    /**
     * Configura el desplazamiento mediante arrastre
     */
    function setupDragScrolling() {
        const container = document.querySelector('.model-container');
        
        container.addEventListener('mousedown', function(e) {
            dragActive = true;
            startX = e.pageX - container.offsetLeft;
            startY = e.pageY - container.offsetTop;
            scrollLeft = container.scrollLeft;
            scrollTop = container.scrollTop;
            
            container.style.cursor = 'grabbing';
        });
        
        container.addEventListener('mouseleave', function() {
            dragActive = false;
            container.style.cursor = 'default';
        });
        
        container.addEventListener('mouseup', function() {
            dragActive = false;
            container.style.cursor = 'default';
        });
        
        container.addEventListener('mousemove', function(e) {
            if (!dragActive) return;
            
            e.preventDefault();
            
            const x = e.pageX - container.offsetLeft;
            const y = e.pageY - container.offsetTop;
            const walkX = (x - startX) * 1.5;
            const walkY = (y - startY) * 1.5;
            
            container.scrollLeft = scrollLeft - walkX;
            container.scrollTop = scrollTop - walkY;
        });
    }
    
    /**
     * Configura el zoom mediante rueda del ratón
     */
    function setupWheelZoom() {
        const container = document.querySelector('.model-container');
        
        container.addEventListener('wheel', function(e) {
            if (e.ctrlKey) {
                e.preventDefault();
                
                if (e.deltaY < 0) {
                    zoomIn();
                } else {
                    zoomOut();
                }
            }
        });
    }
    
    /**
     * Anima la entrada inicial de las entidades
     */
    function animateEntrance() {
        const staggeredItems = document.querySelectorAll('.staggered-item');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('slide-up');
                        entry.target.style.opacity = '1';
                    }, 150 * index);
                }
            });
        }, { threshold: 0.1 });
        
        staggeredItems.forEach(item => {
            observer.observe(item);
        });
    }
    
    /**
     * Actualiza el zoom del modelo
     */
    function updateZoom() {
        modelContent.style.transform = `scale(${scale})`;
    }
    
    /**
     * Aumenta el nivel de zoom
     */
    function zoomIn() {
        if (scale < 1.5) {
            scale += zoomStep;
            updateZoom();
        }
    }
    
    /**
     * Disminuye el nivel de zoom
     */
    function zoomOut() {
        if (scale > 0.5) {
            scale -= zoomStep;
            updateZoom();
        }
    }
    
    /**
     * Restablece el nivel de zoom
     */
    function resetZoom() {
        scale = 1;
        updateZoom();
    }
    
    /**
     * Activa/desactiva el destacado de relaciones
     */
    function toggleRelationshipHighlight() {
        highlightRelationships = !highlightRelationships;
        const relationships = document.querySelectorAll('.relationship');
        const entities = document.querySelectorAll('.entity');
        
        if (highlightRelationships) {
            document.getElementById('toggleRelationships').innerHTML = '<i class="fas fa-project-diagram"></i> Modo Normal';
            
            relationships.forEach(rel => {
                rel.style.backgroundColor = '#e3f2fd';
                rel.style.boxShadow = '0 0 10px rgba(52, 152, 219, 0.5)';
                rel.style.transform = 'scale(1.05)';
            });
            
            // Atenuar entidades
            entities.forEach(entity => {
                entity.style.opacity = '0.7';
            });
        } else {
            document.getElementById('toggleRelationships').innerHTML = '<i class="fas fa-project-diagram"></i> Destacar Relaciones';
            
            relationships.forEach(rel => {
                rel.style.backgroundColor = '#f8f9fa';
                rel.style.boxShadow = 'none';
                rel.style.transform = 'scale(1)';
            });
            
            // Restaurar entidades
            entities.forEach(entity => {
                entity.style.opacity = '1';
            });
        }
    }
    
    /**
     * Destaca una entidad y todas sus relaciones
     */
    function highlightRelatedEntities(entityId) {
        // Eliminar el resaltado anterior
        document.querySelectorAll('.entity').forEach(e => {
            e.style.boxShadow = 'var(--shadow)';
            e.style.transform = 'translateY(0)';
            e.style.opacity = '1';
            e.style.zIndex = '1';
        });
        
        document.querySelectorAll('.relationship').forEach(r => {
            r.style.backgroundColor = '#f8f9fa';
            r.style.transform = 'scale(1)';
        });
        
        // Obtener las entidades relacionadas
        const relatedEntities = entityRelations[entityId] || [];
        
        // Atenuar todas las entidades primero
        document.querySelectorAll('.entity').forEach(e => {
            if (e.id !== entityId && !relatedEntities.includes(e.id)) {
                e.style.opacity = '0.4';
            }
        });
        
        // Destacar la entidad seleccionada
        const selectedEntity = document.getElementById(entityId);
        selectedEntity.style.boxShadow = '0 0 20px rgba(46, 204, 113, 0.7)';
        selectedEntity.style.transform = 'translateY(-10px)';
        selectedEntity.style.zIndex = '10';
        
        // Destacar entidades relacionadas
        relatedEntities.forEach(relId => {
            const relEntity = document.getElementById(relId);
            relEntity.style.boxShadow = '0 0 15px rgba(52, 152, 219, 0.7)';
            relEntity.style.transform = 'translateY(-5px)';
            relEntity.style.zIndex = '5';
        });
        
        // Destacar relaciones relevantes
        const entityName = entityId.replace('entity-', '').toLowerCase();
        
        document.querySelectorAll('.relationship').forEach(r => {
            const relationText = r.textContent.toLowerCase();
            
            if (relationText.includes(entityName)) {
                r.style.backgroundColor = '#e3f2fd';
                r.style.transform = 'scale(1.05)';
                r.style.boxShadow = '0 0 10px rgba(52, 152, 219, 0.3)';
            }
        });
    }
    
    /**
     * Muestra un tooltip con información sobre la entidad
     */
    function showEntityTooltip(entityId) {
        // En una implementación completa, esto mostraría un tooltip
        // con información adicional sobre la entidad
        console.log(`Mostrando tooltip para: ${entityId}`);
    }
    
    /**
     * Oculta el tooltip de entidad
     */
    function hideEntityTooltip() {
        // Oculta el tooltip
    }
    
    /**
     * Genera una imagen exportable del modelo
     */
    function exportModelAsImage() {
        // En un entorno real, aquí implementaríamos la exportación a imagen
        // Usando html2canvas o una biblioteca similar
        
        alert("Funcionalidad de exportación: En un entorno de producción, esta característica permitiría guardar el diagrama como una imagen PNG/PDF");
    }
});

/**
 * Visualizador de flujo de trabajo de tickets
 * Esta función crea una visualización dinámica del ciclo de vida de tickets
 */
function initializeWorkflowVisualizer() {
    const workflowStates = [
        { 
            id: 'creacion', 
            name: 'Creación',
            icon: 'fas fa-plus-circle',
            description: 'Usuario genera un SAR en el sistema'
        },
        { 
            id: 'asignacion', 
            name: 'Asignación',
            icon: 'fas fa-user-check',
            description: 'Ticket asignado a un especialista'
        },
        { 
            id: 'desarrollo', 
            name: 'Desarrollo',
            icon: 'fas fa-code',
            description: 'Implementación de la solución'
        },
        { 
            id: 'pruebas', 
            name: 'Pruebas',
            icon: 'fas fa-vial',
            description: 'Verificación de la solución'
        },
        { 
            id: 'cierre', 
            name: 'Cierre',
            icon: 'fas fa-check-double',
            description: 'Ticket finalizado y documentado'
        }
    ];
    
    // Crear contenedor de flujo de trabajo si existe el elemento
    const workflowContainer = document.getElementById('workflow-visualizer');
    if (workflowContainer) {
        const workflowHTML = document.createElement('div');
        workflowHTML.className = 'workflow-container';
        
        // Crear pasos del flujo
        workflowStates.forEach(state => {
            const step = document.createElement('div');
            step.className = 'workflow-step';
            step.id = `workflow-${state.id}`;
            
            step.innerHTML = `
                <div class="workflow-icon">
                    <i class="${state.icon}"></i>
                </div>
                <div class="workflow-title">${state.name}</div>
                <div class="workflow-desc">${state.description}</div>
            `;
            
            workflowHTML.appendChild(step);
        });
        
        workflowContainer.appendChild(workflowHTML);
    }
} 