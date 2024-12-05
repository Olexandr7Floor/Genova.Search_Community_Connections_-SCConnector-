document.getElementById('searchForm').addEventListener('submit', function(event) {
    const searchQuery = document.getElementById('searchQuery').value.trim();
  
    // Перевірка, чи містить запит лише одну зірочку
    if (searchQuery === '*' || searchQuery === '*?' || searchQuery === '?*' || searchQuery === '*:*' || searchQuery === '' ) {
      alert('Invalid query syntax');
      event.preventDefault(); // Запобігає відправці форми
      location.reload(); // Оновлює сторінку
    }
  });

  const searchButton = document.getElementById('searchButton');
      const loader = searchButton.querySelector('.load');
      const buttonText = searchButton.querySelector('.btn-text');
  function ready() {
    
    loader.style.display = 'none';
    buttonText.style.display = 'inline';
    // зображення ще не завантажено (якщо воно не було кешоване), тому розмір 0x0
    alert(`Image size: ${img.offsetWidth}x${img.offsetHeight}`);
  }

  document.addEventListener("DOMContentLoaded", ready);

  document.getElementById('searchForm').addEventListener('submit', function(event) {


      loader.style.display = 'block';
      buttonText.style.display = 'none';

      // Припустимо, що результат завантажується асинхронно
      // Можливо, ви будете отримувати результати через AJAX або Fetch API
      // Тому ви повинні приховати прелоудер, коли дані завантажено
      // Цей код приклад
      // Примітка: вам потрібно буде модифікувати його відповідно до вашого випадку
 // замініть 3000 мс на час, коли результати завантажуються
  });

  
  function showWarning(event) {
    event.preventDefault(); // Зупинити перехід за посиланням на час попередження
  
    // Показати попередження
    var alertContainer = document.getElementById('alert-container');
    alertContainer.style.display = 'block';
  
    // Зникнення попередження через 3 секунди
    setTimeout(function() {
      alertContainer.style.display = 'none';
      // Після зникнення попередження перейти за посиланням
      window.open(event.target.href, '_blank');
    }, 4000);
  }

  
  document.getElementById('downloadBtnjson').addEventListener('click', function() {
    const link = document.createElement('a');
    link.href = '/queries/dict_.json';
    link.download = 'dict_.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});


function toggleDetails(button) {
    const details = button.closest('.news-item').querySelector('.details');
    if (details.style.display === "none") {
        details.style.display = "block";
        button.textContent = "Less";
    } else {
        details.style.display = "none";
        button.textContent = "More";
    }
}


function getAi() {
    let preloader = document.getElementById("preloader");
    let resultContainer = document.getElementById("result-container");

    if (preloader) {
      // Відображаємо прелоадер
      preloader.style.display = "block";
    }

    let input_text = document.getElementById("prompt_ai").value;

    // Виконуємо запит
    axios.get('/list/ai?sabmit_text=' + encodeURIComponent(input_text))
      .then(function (response) {
        // Обробка успішного запиту
        if (resultContainer) {
resultContainer.innerHTML = `<pre class="formatted-text">${response.data.text_AI}</pre>`;
}

        console.log(response);
      })
      .catch(function (error) {
        // Обробка помилки
        console.log(error);
      })
      .finally(function () {
        // Завжди виконується
        if (preloader) {
          // Ховаємо прелоадер після того, як відповідь отримана
          preloader.style.display = "none";
        }
      });
  }

  document.getElementById('downloadBtnSvg').addEventListener('click', function() {
    var svgFilePath = '/content/other/output_graph.svg';
    var downloadLink = document.createElement("a");
    downloadLink.setAttribute("href", svgFilePath);
    downloadLink.setAttribute("download", "Semantic map.svg");
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });

  function validateForm() {
    const searchQuery = document.getElementById('searchQuery').value.trim();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const errorMessage = document.getElementById('error-message');
    
    if (!searchQuery) {
      errorMessage.textContent = 'Please enter a search query.';
      return false;
    }

    if (!startDate || !endDate) {
      errorMessage.textContent = 'Please select both start and end dates.';
      return false;
    }

    if (new Date(startDate) > new Date(endDate)) {
      errorMessage.textContent = 'Start date cannot be after end date.';
      return false;
    }

    errorMessage.textContent = ''; 
    return true; 
  }


  function toggleInputFields() {
    const method = document.getElementById("dataInputMethod").value;
    const discordFields = document.getElementById("discordFields");
    const telegramFields = document.getElementById("telegramFields");

    if (method === "discord") {
      discordFields.style.display = "block";
      telegramFields.style.display = "none";
    } else if (method === "telegram") {
      discordFields.style.display = "none";
      telegramFields.style.display = "block";
    }
  }
  
  // Ініціалізація, щоб відразу відобразити правильні поля
  toggleInputFields();


  document.getElementById('uploadBtn').addEventListener('click', function() {
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    
    if (fileInput.files.length > 0) {
      formData.append('fileInput', fileInput.files[0]);
      
      axios.post('/upload', formData)
        .then(function(response) {
          alert('Файл завантажено: ' + response.data);
        })
        .catch(function(error) {
          console.error('Error:', error);
          alert('Сталася помилка при завантаженні файлу.');
        });
    } else {
      alert('Будь ласка, виберіть файл для завантаження.');
    }
  });

