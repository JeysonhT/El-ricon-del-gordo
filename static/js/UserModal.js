// Obtener los elementos
const modal = document.getElementById("crearUsuarioModal");
const btnAbrir = document.getElementById("crearUsuario");
const btnCerrar = document.querySelector(".cerrar");
const editBtns = document.querySelectorAll(".edit-btn");

const modalTitle = document.getElementById("modal-title");
const modalForm = document.getElementById("modal-form");
const submitBtn = document.getElementById("submit-btn");
const userIdInput = document.getElementById("user_id");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const roleInput = document.getElementById("role");
const passwordInput = document.getElementById("password");

// 1. Cuando el usuario hace clic en el botón de abrir para crear
btnAbrir.addEventListener("click", () => {
  modalTitle.textContent = "Crear Usuario";
  modalForm.action = "/create-user";
  submitBtn.value = "Guardar Usuario";
  userIdInput.value = "";
  nameInput.value = "";
  emailInput.value = "";
  roleInput.value = "1";
  passwordInput.required = true;
  modal.classList.add("modal-active");
});

// 2. Cuando el usuario hace clic en un botón de editar
editBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        modalTitle.textContent = "Editar Usuario";
        modalForm.action = "/update-user";
        submitBtn.value = "Guardar Cambios";

        userIdInput.value = btn.dataset.id;
        nameInput.value = btn.dataset.name;
        emailInput.value = btn.dataset.email;
        roleInput.value = btn.dataset.role;
        passwordInput.required = false;

        modal.classList.add("modal-active");
    });
});

// 3. Cuando el usuario hace clic en la "X" para cerrar
btnCerrar.addEventListener("click", () => {
  modal.classList.remove("modal-active");
});

// 4. Cuando el usuario hace clic en cualquier lugar fuera del modal, cerrarlo
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.classList.remove("modal-active");
  }
});

// --- Lógica para el modal de confirmación de eliminación ---

const deleteModal = document.getElementById("deleteConfirmModal");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
const closeDeleteModal = document.querySelector(".cerrar-delete");
let userIdToDelete = null;

function confirmDelete(userId) {
  userIdToDelete = userId;
  deleteModal.style.display = "flex"; // Usamos flex para centrar con el CSS añadido
}

confirmDeleteBtn.addEventListener("click", () => {
  if (userIdToDelete) {
    document.getElementById('delete-form-' + userIdToDelete).submit();
  }
});

function closeConfirmModal() {
    deleteModal.style.display = "none";
    userIdToDelete = null;
}

cancelDeleteBtn.addEventListener("click", closeConfirmModal);
closeDeleteModal.addEventListener("click", closeConfirmModal);

window.addEventListener("click", (event) => {
  if (event.target == deleteModal) {
    closeConfirmModal();
  }
});
