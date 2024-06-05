// calendar.js

// 쿠키를 가져오는 함수
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // 쿠키 이름이 일치하면 값을 반환
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 이미지를 미리보는 함수
function readURL(input, previewId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            // 이미지 미리보기 설정
            document.getElementById(previewId).style.display = 'block';
            document.getElementById(previewId).src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]);
    }
}

// 페이지 로드 시 실행
window.onload = function() {
    // 날짜 클릭 이벤트 설정
    document.querySelectorAll('.date').forEach(function(dateElement) {
        // 마우스 커서 모양 변경을 위한 CSS 클래스 추가
        dateElement.classList.add('cursor-pointer');

        dateElement.addEventListener('click', function(e) {
            var date = e.target.dataset.date;
            var eventId = e.target.dataset.eventId;  // 이벤트 ID (수정 가능 여부 확인을 위해 사용)
            var isEditable = e.target.dataset.isEditable;  // 수정 가능 여부
            // 이벤트 ID가 있고 수정 불가능하면 이벤트 페이지로, 그렇지 않으면 새 이벤트 페이지로 이동
            if (eventId && !isEditable) {
                window.location.href = '/event/' + eventId + '?date=' + date;  // 페이지 이동
            } else {
                window.location.href = '/event/new?date=' + date;  // 페이지 이동
            }
        });
    });

    // 이미지 미리보기 이벤트 설정
    ['outer_clothes', 'top_clothes', 'bottom_clothes'].forEach(function(clothesType) {
        var clothesInput = document.getElementById('id_' + clothesType);
        if (clothesInput && !clothesInput.disabled) {
            clothesInput.addEventListener('change', function() {
                readURL(this, clothesType + '_preview');
            });
        }
    });
}

function getWeather(lat, lon) {
    fetch(`/weather/?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            var weatherText = document.getElementById('weatherText');
            weatherText.innerText = 'Temperature: ' + data.temp + ', Description: ' + data.description;

            var weatherIcon = document.getElementById('weatherIcon');
            weatherIcon.src = "http://openweathermap.org/img/w/" + data.icon + ".png";
        });
}