const express = require('express');
const app = express();

// Cấu hình máy chủ đọc được dữ liệu dạng JSON gửi lên
app.use(express.json());

// Thiết lập cổng chạy máy chủ (Mặc định là 3000 hoặc theo cấu hình của Render/Vercel)
const PORT = process.env.PORT || 3000;

/**
 * 1. TẠO ĐƯỜNG DẪN /kio/web/mcp THEO Ý BẠN
 * Khi OpenAI Agent gửi yêu cầu kết nối (POST) đến link này, máy chủ sẽ xử lý.
 */
app.post('/kio/web/mcp', (req, res) => {
    
    // ĐỌC ĐÚNG TÊN TIÊU ĐỀ (Giữ nguyên chữ x-consumer-api-key viết thường)
    const apiKeyHeader = req.headers['x-consumer-api-key'];
    
    // MÃ KHÓA BÍ MẬT CỦA BẠN (Đã điền đúng)
    const MY_SECRET_API_KEY = 'ck_xzjvfyyC-YhtIrwv3jsV';

    // Kiểm tra xem OpenAI có gửi khóa lên không và khóa có trùng khớp không
    if (!apiKeyHeader || apiKeyHeader !== MY_SECRET_API_KEY) {
        return res.status(401).json({ 
            status: "error", 
            message: "Xác thực thất bại! Khóa x-consumer-api-key không chính xác." 
        });
    }

    // Nếu khóa chính xác, trả về phản hồi thành công cho OpenAI Agent
    return res.json({
        status: "success",
        message: "Kết nối máy chủ MCP thành công!",
        mcp_version: "1.0.0",
        capabilities: {
            tools: {},
            resources: {}
        }
    });
});

/**
 * 2. TẠO THÊM ĐƯỜNG DẪN GỐC (Trang chủ)
 * Để khi bạn bấm vào link gốc (Ví dụ: https://kio-ai.onrender.com) không bị lỗi màn hình trắng.
 */
app.get('/', (req, res) => {
    res.send('<h1>Máy chủ MCP đang hoạt động bình thường!</h1>');
});

// Khởi chạy máy chủ
app.listen(PORT, () => {
    console.log(`Máy chủ MCP của bạn đang chạy mượt mà tại cổng ${PORT}`);
});
