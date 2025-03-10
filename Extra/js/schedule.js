
const form = document.querySelector('form');
const nameInput = document.getElementById('meetingName');
const idInput = document.getElementById('meetingId');
const dateInput = document.getElementById('meetingDate');
const timeInput = document.getElementById('meetingTime');

form.addEventListener('submit', e => {

    const name = nameInput.value;
    const id = idInput.value;
    const date = dateInput.value;
    const time = timeInput.value;

    if (!name || !id || !date || !time) {
        alert('Enter details');
        return;
    }

    const meetings = document.querySelector('.meetings-container');

    const meeting = document.createElement('div');
    meeting.classList.add('meeting-item');

    meeting.innerHTML = `
    <strong>${name}</strong>
    <p>ID: ${id}</p>
    <p>${date} at ${time}</p>
  `;

    const joinButton = document.createElement('button');
    joinButton.textContent = 'Join Meeting';

    joinButton.addEventListener('click', () => {
        window.location.href = 'lobby.html';
    });

    meeting.appendChild(joinButton);

    meetings.appendChild(meeting);

    form.reset();

    e.preventDefault();
});