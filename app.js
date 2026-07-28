let studentData = [];
let isDataLoaded = false;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const statusDiv = document.getElementById('status');
const statusText = document.getElementById('statusText');
const resultsContainer = document.getElementById('resultsContainer');
const resultsCount = document.getElementById('resultsCount');
const cardsWrapper = document.getElementById('cardsWrapper');

// Start parsing the CSV file immediately
Papa.parse("data.csv", {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function(results) {
        studentData = results.data;
        isDataLoaded = true;
        
        // Update UI
        statusDiv.className = 'status success';
        statusDiv.innerHTML = '✅ <span id="statusText">تم تحميل البيانات بنجاح! جاهز للبحث.</span>';
        searchBtn.disabled = false;
        searchInput.focus();
    },
    error: function(err) {
        statusDiv.className = 'status error';
        statusDiv.innerHTML = '❌ <span id="statusText">حدث خطأ أثناء تحميل البيانات. يرجى تحديث الصفحة.</span>';
        console.error("PapaParse Error:", err);
    }
});

// Event Listeners for Search
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

function performSearch() {
    if (!isDataLoaded) return;
    
    const query = searchInput.value.trim();
    if (!query) {
        alert('يرجى إدخال اسم أو رقم جلوس للبحث');
        return;
    }
    
    resultsContainer.classList.remove('hidden');
    cardsWrapper.innerHTML = '';
    
    const isNumber = /^\d+$/.test(query);
    let matchedResults = [];
    
    if (isNumber) {
        // Exact match for seating number
        matchedResults = studentData.filter(row => row.seating_no === query);
    } else {
        // Partial match for name
        matchedResults = studentData.filter(row => row.arabic_name && row.arabic_name.includes(query));
    }
    
    // Render Results
    if (matchedResults.length === 0) {
        resultsCount.textContent = 'لم يتم العثور على طالب بهذا الاسم أو رقم الجلوس.';
        resultsCount.style.color = '#ff4d4d';
    } else {
        resultsCount.textContent = `تم العثور على ${matchedResults.length} نتيجة:`;
        resultsCount.style.color = 'var(--primary-color)';
        
        // Limit rendering to 100 results to prevent browser freezing if query is too generic
        const limit = Math.min(matchedResults.length, 100);
        
        for (let i = 0; i < limit; i++) {
            const row = matchedResults[i];
            const card = document.createElement('div');
            card.className = 'card';
            
            card.innerHTML = `
                <div class="card-row">
                    <span class="card-label">الاسم:</span>
                    <span class="card-value highlight">${row.arabic_name || 'غير متوفر'}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">رقم الجلوس:</span>
                    <span class="card-value">${row.seating_no || 'غير متوفر'}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">المجموع:</span>
                    <span class="card-value highlight">${row.total_degree || 'غير متوفر'}</span>
                </div>
                <div class="card-row">
                    <span class="card-label">الحالة:</span>
                    <span class="card-value">${row.student_case_desc || 'غير متوفر'}</span>
                </div>
            `;
            cardsWrapper.appendChild(card);
        }
        
        if (matchedResults.length > 100) {
            const msg = document.createElement('p');
            msg.style.textAlign = 'center';
            msg.style.color = '#ffc107';
            msg.style.marginTop = '10px';
            msg.textContent = 'تم عرض أول 100 نتيجة فقط. يرجى كتابة الاسم بشكل أدق.';
            cardsWrapper.appendChild(msg);
        }
    }
}
