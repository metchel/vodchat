const state = {
    modal: {
        open: false,
        videoId: null,
        ref: null
    },
};

function deleteVideo(videoId, videoName, thumbnail) {
    state.modal.ref = openModal(videoId, videoName, thumbnail);
}

function editVideo(videoId, videoName) {
    state.tabs.edit.click();
    selectVideo(videoId, videoName, videoDescription);
}

function openModal(videoId, videoName, thumbnail) {
    const confirmDeleteModal = document.getElementById("confirmDeleteModal");
    const confirmMessage = document.getElementById("confirmMessage");
    const deleteThumb = document.getElementById("deleteThumb");
    deleteThumb.src = thumbnail;
    confirmMessage.innerHTML = "Are you sure you want to delete <strong><em>&quot;" + videoName + "&quot;</em></strong> ?"
    confirmDeleteModal.style.display = 'block';
    state.modal.open = true;
    state.modal.videoId = videoId;

    return confirmDeleteModal;
}

function closeModal() {
    state.modal.ref.style.display = 'none';
    state.modal.open = false;
    state.modal.ref = null;
    state.modal.videoId = null;
}

function confirm() {
    const videoListItem = document.getElementById("video-" + state.modal.videoId);
    fetch('/videos/delete?video_id=' + state.modal.videoId)
        .then(res => res.json())
        .then(json => {
            console.log(json);
            videoListItem.style.display = 'none';
        });
    closeModal();
}

function cancel() {
    closeModal();
}