# latex-template: khung LaTeX báo cáo HCMUT

Khung sườn rút từ `reports/master/` (class `hcmut-report`, bìa, header, môi trường `usecase`), mỗi định dạng có **một ví dụ ngắn** lấy từ báo cáo JobQuest để thấy chỗ nào viết gì và trông ra sao. Dùng để bắt đầu một báo cáo khác với cùng định dạng. Bản gốc trong `reports/` không bị sửa. Build thử ra PDF 15 trang, không lỗi.

## Cấu trúc và chỗ cần thay

| File | Nội dung mẫu | Thay thế thế nào |
|---|---|---|
| `hcmut-report.cls` | Class: khổ giấy, lề, header/footer, bìa, đánh số | **Không sửa** (chép nguyên văn từ bản gốc) |
| `graphics/hcmut.png` | Logo trên bìa và header (đường dẫn cố định trong class) | Giữ nguyên |
| `main.tex` | Preamble + thông tin bìa JobQuest + 4 dòng `\input{chapters/…}` | Giữ phần preamble, **sửa khối `\coursename` … `\stuname`**, thêm/bớt dòng `\input` |
| `chapters/00-abstract.tex` | Abstract + Keywords | Viết lại 2 đoạn và dòng `\textbf{Keywords:}` |
| `chapters/00-list-of-abbreviations.tex` | Bảng viết tắt (3 dòng mẫu) | Thay các dòng `ABC & Expansion \\ \hline`, giữ khung bảng |
| `chapters/ch1.tex` | Chương 1: mục `\subsection`/`\subsubsection`, `\cite`, danh sách `enumerate` | Viết lại nội dung, giữ cấu trúc mục |
| `chapters/ch2.tex` | Chương 2: bảng thường `longtable` có caption (2 hàng) | Thay đoạn văn; copy khối `{\small \begin{longtable}…}` cho bảng mới |
| `chapters/ch3.tex` | Chương 3: bảng so sánh rộng trên trang landscape (3 hàng, 4 cột), chú thích ký hiệu | Thay các hàng; đổi số cột `*{3}{p{5.9cm}}` cho khớp. Cột đầu 3,1 cm; các cột còn lại chia đều sao cho tổng khoảng 21 cm (7 cột thì mỗi cột 2,55 cm, 3 cột thì 5,9 cm). Header nằm dọc bên phải trên trang landscape là hành vi của class, không phải lỗi |
| `chapters/ch4.tex` | Chương 4: một hình dọc, một bảng use case `usecase`, một hình ngang trên trang landscape | Thay ảnh, caption và nội dung use case |
| `references.tex` | 5 mục `\bibitem{r1}`–`\bibitem{r5}` (sách, bài báo, chương sách) | Thay bằng tài liệu thật; chỉnh số trong `\begin{thebibliography}{N}` |
| `figures/` | Ảnh mẫu: `AD-01a…` và `SITE-02…` dùng trong `ch4.tex`; `UC-00…` hiện chưa dùng | Xoá ảnh mẫu, bỏ ảnh mới vào |

## Dùng cho báo cáo mới

1. Chép cả folder sang chỗ mới, ví dụ `reports/<ngày>_<slug>/`.
2. Sửa khối thông tin bìa trong `main.tex`.
3. Viết lại từng file trong `chapters/` theo bảng trên. Mỗi chương bắt đầu bằng `\newpage` rồi `\section{…}`.
4. Thay `references.tex`. Số `rN` trong `\cite{rN}` phải khớp `\bibitem{rN}`.
5. Build: `latexmk -pdf -outdir=build main.tex` (PDF ở `build/main.pdf`). Cần MiKTeX/TeX Live có `longtable-2020-01-07.sty`; nếu thiếu, xoá dòng `\declare@file@substitution` ở đầu `main.tex`.

## Cú pháp hay dùng (có ví dụ sẵn trong mẫu)

- **Trích dẫn:** `\cite{r1}`, nhiều nguồn `\cite{r1,r2}`. Hiện dạng chỉ số mũ `[1]` (natbib, `super`).
- **Hình dọc:** `figure[H]` + `\includegraphics[width=0.59\textwidth,height=0.85\textheight,keepaspectratio]{figures/<tên>.png}` + `\caption{…}` (ví dụ ở `ch4.tex`).
- **Hình/bảng ngang:** bọc trong `\begin{landscape}…\end{landscape}`; hình dùng `width=\linewidth`.
- **Bảng thường:** `{\small \begin{longtable}…}` với caption **trên** bảng, độ rộng cột là phân số của `\textwidth` (ví dụ ở `ch2.tex`).
- **Bảng use case:** `\begin{usecase}{UC-xx}{Tên}` với `\ucrow`, `\ucsteps`, `\ucstep`, `\ucitem` (ví dụ ở `ch4.tex`).
- **Gạch ngang dài** `---`, khoảng số `--`.

## Lưu ý

- Các câu kiểu "Section 4.2.2", "Chapter 4" trong văn bản mẫu là chữ viết tay trỏ tới các chương của báo cáo đầy đủ, không phải `\ref`. Khung này chỉ có 4 chương nên các số đó không khớp; sửa khi viết lại.
- Chương trong khung chỉ là ví dụ cú pháp, không phải cấu trúc bắt buộc. Báo cáo ĐACN thì tên chương/mục theo `docs/project-hub/templates/bao-cao-dacn.md`.
- Folder này không có `report.md` và không dùng `tools/report/md2tex.py`: viết trực tiếp bằng LaTeX.
