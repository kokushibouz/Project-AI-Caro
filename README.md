# AI chơi Cờ Caro sử dụng Thuật toán Minimax với Cắt tỉa Alpha-Beta

Dự án này triển khai một AI chơi cờ Caro (tic-tac-toe) sử dụng thuật toán **Minimax** kết hợp với **Alpha-Beta Pruning** để tối ưu hóa việc tìm kiếm và giảm số lượng trạng thái cần kiểm tra trong quá trình tìm kiếm các nước đi tốt nhất.

## Tổng quan Dự án

Cờ Caro là một trò chơi phổ biến, trong đó hai người chơi (hoặc một người chơi và máy) lần lượt đánh dấu các ô trên bảng 3x3 với mục tiêu xếp 3 ký tự liên tiếp theo chiều ngang, dọc hoặc chéo. AI trong dự án này sử dụng thuật toán Minimax để quyết định nước đi tối ưu, và áp dụng cắt tỉa Alpha-Beta để tăng hiệu suất tìm kiếm.

### Các thuật toán sử dụng:
- **Minimax Algorithm**: Thuật toán tìm kiếm để tối ưu hóa nước đi của người chơi bằng cách đánh giá các tình huống trên bàn cờ từ trạng thái hiện tại đến các trạng thái kết thúc (kết quả thắng, hòa hoặc thua).
- **Alpha-Beta Pruning**: Là một kỹ thuật cắt tỉa để tối ưu hóa thuật toán Minimax, giảm thiểu số lượng nút cần kiểm tra trong cây tìm kiếm, từ đó tăng tốc độ tính toán.
