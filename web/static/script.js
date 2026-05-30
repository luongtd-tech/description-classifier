// Xử lý chuyển tab
function switchTab(tabId) {
    // Ẩn tất cả nội dung tab
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Bỏ active tất cả nút tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Kích hoạt tab được chọn
    document.getElementById(`${tabId}-tab`).classList.add('active');
    
    // Kích hoạt nút tab tương ứng (tìm button chứa text tương ứng hoặc có thể thêm id cho button)
    const btns = document.querySelectorAll('.tab-btn');
    if (tabId === 'single') {
        btns[0].classList.add('active');
    } else {
        btns[1].classList.add('active');
    }
}

// Xử lý hiển thị tên file khi chọn file
const fileInput = document.getElementById('file-input');
const fileMsg = document.querySelector('.file-msg');

fileInput.addEventListener('change', function(e) {
    if (this.files && this.files.length > 0) {
        fileMsg.textContent = `Đã chọn file: ${this.files[0].name}`;
        fileMsg.style.color = 'var(--text-primary)';
    } else {
        fileMsg.textContent = 'Kéo thả file vào đây hoặc click để chọn file CSV/TXT';
        fileMsg.style.color = 'var(--text-secondary)';
    }
});

// Xử lý submit form dự đoán đơn lẻ
document.getElementById('single-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const textInput = document.getElementById('text-input').value;
    const btn = document.getElementById('predict-btn');
    const resultBox = document.getElementById('single-result');
    
    // Trạng thái loading
    const originalBtnHTML = btn.innerHTML;
    btn.innerHTML = 'Đang Xử Lý... <i class="fa-solid fa-spinner"></i>';
    btn.disabled = true;
    resultBox.classList.add('hidden');
    
    try {
        const formData = new FormData();
        formData.append('text', textInput);
        
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            renderSingleResult(data.result, resultBox);
        } else {
            resultBox.innerHTML = `<div class="error" style="color: var(--error);"><i class="fa-solid fa-triangle-exclamation"></i> ${data.error || 'Có lỗi xảy ra'}</div>`;
            resultBox.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        resultBox.innerHTML = `<div class="error" style="color: var(--error);"><i class="fa-solid fa-triangle-exclamation"></i> Không thể kết nối tới server</div>`;
        resultBox.classList.remove('hidden');
    } finally {
        btn.innerHTML = originalBtnHTML;
        btn.disabled = false;
    }
});

function renderSingleResult(result, container) {
    const { predicted_label, probabilities, comment } = result;
    
    // Sort probabilities để hiển thị thanh phần trăm
    const sortedProbs = Object.entries(probabilities)
        .sort((a, b) => b[1] - a[1]);
        
    let probBarsHTML = '';
    sortedProbs.forEach(([label, prob]) => {
        probBarsHTML += `
            <div class="prob-bar-container">
                <span class="prob-text">${label}</span>
                <div class="prob-bar" style="width: 0%" data-width="${prob}%"></div>
                <span class="prob-value">${prob}%</span>
            </div>
        `;
    });
    
    container.innerHTML = `
        <div class="result-header">
            <h3>Kết quả dự đoán:</h3>
            <span class="badge ${getBadgeClass(predicted_label)}"><i class="fa-solid fa-tag"></i> ${predicted_label}</span>
        </div>
        <div class="probabilities">
            ${probBarsHTML}
        </div>
        <div class="comment">
            <i class="fa-solid fa-lightbulb" style="color: #fbbf24; margin-right: 5px;"></i>
            ${comment}
        </div>
    `;
    
    container.classList.remove('hidden');
    
    // Animation cho progress bar
    setTimeout(() => {
        const bars = container.querySelectorAll('.prob-bar');
        bars.forEach(bar => {
            bar.style.width = bar.getAttribute('data-width');
        });
    }, 50);
}

// Xử lý upload file batch
document.getElementById('batch-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        alert('Vui lòng chọn file!');
        return;
    }
    
    const btn = document.getElementById('batch-btn');
    const resultBox = document.getElementById('batch-result');
    
    // Trạng thái loading
    const originalBtnHTML = btn.innerHTML;
    btn.innerHTML = 'Đang Xử Lý File... <i class="fa-solid fa-spinner"></i>';
    btn.disabled = true;
    resultBox.classList.add('hidden');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/predict_batch', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            renderBatchResult(data, resultBox);
        } else {
            resultBox.innerHTML = `<div class="error" style="color: var(--error);"><i class="fa-solid fa-triangle-exclamation"></i> ${data.error || 'Có lỗi xảy ra'}</div>`;
            resultBox.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        resultBox.innerHTML = `<div class="error" style="color: var(--error);"><i class="fa-solid fa-triangle-exclamation"></i> Không thể kết nối tới server</div>`;
        resultBox.classList.remove('hidden');
    } finally {
        btn.innerHTML = originalBtnHTML;
        btn.disabled = false;
    }
});

function renderBatchResult(data, container) {
    const { filename, total_processed, results } = data;
    
    let rowsHTML = '';
    results.forEach((item, index) => {
        rowsHTML += `
            <tr>
                <td>${index + 1}</td>
                <td class="text-cell" title="${item.text}">${item.text}</td>
                <td class="label-cell"><span class="badge ${getBadgeClass(item.predicted_label)}" style="font-size: 0.9rem; padding: 0.2rem 0.6rem;">${item.predicted_label}</span></td>
                <td>${item.probabilities[item.predicted_label]}%</td>
            </tr>
        `;
    });
    
    container.innerHTML = `
        <div class="result-header">
            <h3><i class="fa-solid fa-check-circle" style="color: var(--success);"></i> Đã xử lý thành công</h3>
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            File: <strong>${filename}</strong> | Tổng số dòng: <strong>${total_processed}</strong>
        </p>
        
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th width="10%">STT</th>
                        <th width="60%">Nội dung mô tả</th>
                        <th width="20%">Phân loại</th>
                        <th width="10%">Độ tin cậy</th>
                    </tr>
                </thead>
                <tbody>
                    ${rowsHTML}
                </tbody>
            </table>
        </div>
    `;
    
    container.classList.remove('hidden');
}

function getBadgeClass(label) {
    const map = {
        "Điện thoại": "badge-dienthoai",
        "Máy tính": "badge-maytinh",
        "Thời trang": "badge-thoitrang",
        "Mỹ phẩm": "badge-mypham",
        "Đồ gia dụng": "badge-dogiadung"
    };
    return map[label] || "";
}

