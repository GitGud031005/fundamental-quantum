# Speaker script — "From quantum foundations to QSVT" / Kịch bản thuyết trình song ngữ

45 minutes (42 of content, 3 of buffer), three speakers; Q&A is separate. Each block gives the slide, the time it starts, what to say in English (**EN**) and the same content in Vietnamese (**VI**) for rehearsal. Lines in *italics* are actions, not speech. Numbers match the notebook outputs; if a re-run gives slightly different digits, read the ones on screen.

45 phút (42 phút nội dung, 3 phút đệm), ba người nói; hỏi đáp tính riêng. Mỗi khối ghi slide, mốc thời gian, lời nói tiếng Anh (**EN**) và bản tiếng Việt (**VI**) để tập. Dòng *in nghiêng* là thao tác, không phải lời nói. Số liệu khớp output của notebook; nếu chạy lại ra chữ số hơi khác thì đọc số trên màn hình.

| Speaker | Slides | Time | Demo |
|---|---|---|---|
| Speaker 1 / Người nói 1 | 1–15 | 00:00–13:00 | Demo 0, `demo0_foundations_grover.ipynb` |
| Speaker 2 / Người nói 2 | 16–28 | 13:00–27:00 | Demo 1, `demo1_qsp_phases.ipynb`; Demo 2, `demo2_qsvt_circuit_measure.ipynb` |
| Speaker 3 / Người nói 3 | 29–47 | 27:00–42:00 | Demo 4, `demo4_bigdata.ipynb` (Demo 3 is backup only) |


---

## Speaker 1 / Người nói 1 — Big data, foundations, classic algorithms (00:00–13:00)

### Slide 1 — Cover · 00:00 (30 s)

**EN:** Good morning. Our project is "From quantum foundations to QSVT". We rebuild classic quantum algorithms inside one framework, the quantum singular value transformation, check every claim by simulation, and ask what it means for big data.

**VI:** Xin chào thầy cô và các bạn. Đề tài của nhóm là "Từ toán nền lượng tử đến QSVT". Nhóm tái dựng các thuật toán lượng tử kinh điển trong một khung chung là biến đổi giá trị kỳ dị lượng tử, kiểm tra mọi khẳng định bằng mô phỏng, và hỏi xem điều đó có ý nghĩa gì với dữ liệu lớn.

### Slide 2 — 10¹² entries · 00:30 (60 s)

**EN:** Start with a number. A recommendation system with a million users and a million items is a rating matrix with 10¹² entries. Most of what we do with such data, fitting, compressing, recommending, searching, is linear algebra on matrices of this size.

**VI:** Bắt đầu bằng một con số. Một hệ khuyến nghị có một triệu người dùng và một triệu sản phẩm là một ma trận đánh giá 10¹² ô. Phần lớn việc ta làm với dữ liệu này, khớp mô hình, nén, khuyến nghị, tìm kiếm, đều là đại số tuyến tính trên ma trận cỡ đó.

### Slide 3 — Big data is linear algebra · 01:30 (60 s)

**EN:** Four everyday tasks. Regression solves beta equals X-plus y. PCA keeps the largest singular values of X. Recommendation samples from a low-rank approximation of the ratings. Search finds the marked rows. Each one is a function of a matrix, which is exactly what QSVT computes.

**VI:** Bốn bài toán quen thuộc. Hồi quy là giải β = X⁺y. PCA là giữ các giá trị kỳ dị lớn nhất của X. Khuyến nghị là lấy mẫu từ một xấp xỉ hạng thấp của ma trận đánh giá. Tìm kiếm là tìm các dòng được đánh dấu. Cả bốn đều là một hàm của ma trận, đúng thứ QSVT tính.

### Slide 4 — Statement · 02:30 (30 s)

**EN:** Grover search, Hamiltonian simulation and solving linear systems look like three very different algorithms. Our main message is that they are the same circuit. The only thing that changes is the polynomial we choose.

**VI:** Tìm kiếm Grover, mô phỏng Hamiltonian và giải hệ tuyến tính trông như ba thuật toán rất khác nhau. Thông điệp chính của nhóm là chúng dùng cùng một mạch. Thứ duy nhất thay đổi là đa thức được chọn.

### Slide 5 — Outline · 03:00 (40 s)

**EN:** The talk has five chapters. Foundations answers RQ0: which math is enough. Classic algorithms shows the four algorithms QSVT will absorb. QSP and QSVT answers RQ1: why rotations give polynomials, even for whole matrices. Algorithms answers RQ2 and RQ3: degrees and comparisons. Big Data answers RQ4: what QSVT actually buys a data system. Every result is checked on Qiskit Aer and numpy with a pass criterion.

**VI:** Bài gồm năm chương. Toán nền trả lời RQ0: phần toán nào là đủ. Thuật toán gốc giới thiệu bốn thuật toán mà QSVT sẽ bao trùm. QSP và QSVT trả lời RQ1: vì sao phép quay tạo ra đa thức, kể cả cho cả ma trận. Ba thuật toán trả lời RQ2 và RQ3: bậc và so sánh. Big Data trả lời RQ4: QSVT thật sự mang lại gì cho một hệ thống dữ liệu. Mọi kết quả đều kiểm tra trên Qiskit Aer và numpy với tiêu chí đạt cụ thể.

### Slide 6 — Section 01 Foundations · 03:40 (10 s)

**EN:** First, the foundations.

**VI:** Trước hết là phần toán nền.

### Slide 7 — What QSVT trains, what it skips · 03:50 (50 s)

**EN:** QSVT is a good summit to climb because it uses almost all of quantum linear algebra: spectra, the SVD, matrix functions, reflections and SU(2). But it never touches density matrices, quantum channels or trace distance, and it uses measurement only indirectly. So in Stage 0 we studied those separately, topics A5 to A8. QSVT trains one half of the math; Stage 0 adds the other half.

**VI:** QSVT là "đỉnh tổng hợp" tốt vì nó dùng gần như toàn bộ đại số tuyến tính lượng tử: phổ, SVD, hàm ma trận, phép phản xạ và SU(2). Nhưng nó không đụng tới ma trận mật độ, kênh lượng tử hay trace distance, và chỉ dùng đo lường gián tiếp. Vì vậy ở Giai đoạn 0 nhóm học riêng các phần đó, từ A5 đến A8. QSVT luyện một nửa phần toán; Giai đoạn 0 bù nửa còn lại.

### Slide 8 — The state-space toolkit · 04:40 (60 s)

**EN:** Five tools in one slide. Global phase cannot be measured, relative phase can. In Qiskit qubit 0 is the rightmost bit, and a Bell state has rank 2, so it is entangled. A matrix function applies f to the eigenvalues. The SVD writes A as a sum of sigma u v-dagger, and QSVT transforms the sigmas. And every SU(2) rotation is cos theta times I plus i sin theta times n dot sigma. In short, QSVT is applying a polynomial to a spectrum.

**VI:** Năm công cụ trong một slide. Pha toàn cục không đo được, pha tương đối thì đo được. Trong Qiskit qubit 0 là bit phải nhất, và trạng thái Bell có hạng 2 nên là trạng thái rối. Hàm ma trận áp f lên các trị riêng. SVD viết A thành tổng σ|u⟩⟨v|, và QSVT biến đổi các σ. Mọi phép quay SU(2) đều có dạng cos θ·I + i sin θ·n·σ. Tóm lại, QSVT là áp một đa thức lên phổ.

### Slide 9 — Three easy-to-miss conventions · 05:40 (40 s)

**EN:** Three conventions caused real bugs for us. First, qubit order: in Qiskit, qubit 0 is the rightmost bit, so we always put the ancilla on the highest index. Second, the sign of R_Z: e to the i phi Z equals R_Z of minus two phi; get the sign wrong and every QSP result is wrong. Third, gate order: matrix products read right to left, so we append gates to the circuit in reverse.

**VI:** Ba quy ước đã gây lỗi thật cho nhóm. Thứ nhất, thứ tự qubit: trong Qiskit qubit 0 là bit phải nhất, nên ancilla luôn đặt ở chỉ số cao nhất. Thứ hai, dấu của R_Z: e mũ i phi Z bằng R_Z của trừ hai phi; sai dấu là sai toàn bộ QSP. Thứ ba, thứ tự cổng: tích ma trận đọc từ phải sang trái, nên phải append cổng vào mạch theo thứ tự đảo.

### Slide 10 — Measuring and post-selecting · 06:20 (40 s)

**EN:** One formula from measurement comes back later. If a unitary block-encodes A over alpha, the probability that the ancilla reads zero is the norm of A psi squared, over alpha squared. For A equal to diag of 0.5 and 0.1 and psi equal to plus, that is 0.13. Also, a circuit of T gates, each off by epsilon, shifts any probability by at most T epsilon. Demo 2 will measure this formula on Aer.

**VI:** Có một công thức về đo lường sẽ quay lại về sau. Nếu một unitary block-encode A chia alpha, xác suất ancilla bằng 0 là chuẩn của A psi bình phương, chia alpha bình phương. Với A = diag(0,5; 0,1) và psi = |+⟩, kết quả là 0,13. Ngoài ra, mạch có T cổng, mỗi cổng sai epsilon, làm lệch mọi xác suất tối đa T nhân epsilon. Demo 2 sẽ đo lại công thức này trên Aer.

### Slide 11 — Mixed states and noise · 07:00 (60 s)

**EN:** QSVT never needs mixed states, but we do. A density matrix is positive with trace one, and its purity lies between 1 over d and 1. Tracing out half of a Bell pair leaves I over 2, maximal ignorance. The Schmidt decomposition is just an SVD, and the Werner state becomes entangled exactly when p exceeds one third. Noise is written with Kraus operators; we checked bit-flip, dephasing, depolarizing and amplitude damping. This is the language for an unmeasured ancilla and for noise.

**VI:** QSVT không cần trạng thái hỗn hợp, nhưng nhóm thì cần. Ma trận mật độ là ma trận dương có vết bằng 1, độ tinh khiết nằm giữa 1/d và 1. Lấy vết riêng phần một nửa cặp Bell còn lại I/2, tức không biết gì. Phân rã Schmidt chính là SVD, và trạng thái Werner rối đúng khi p lớn hơn 1/3. Nhiễu được viết bằng toán tử Kraus; nhóm đã kiểm tra bit-flip, dephasing, depolarizing và amplitude damping. Đây là ngôn ngữ để nói về ancilla chưa đo và về nhiễu.

### Slide 12 — Telling states apart · 08:00 (50 s)

**EN:** Helstrom's theorem: the best single measurement tells rho from sigma with probability one half plus half the trace distance. For zero and plus, that is cos squared pi over 8, about 0.854. No channel can increase the trace distance. And if two circuits differ by epsilon, every measured probability moves by at most epsilon, so T gates each off by epsilon cost at most T epsilon. That is how a polynomial error in QSVT becomes an error in what we measure.

**VI:** Định lý Helstrom: phép đo tốt nhất phân biệt ρ với σ với xác suất bằng một nửa cộng một nửa khoảng cách vết. Với |0⟩ và |+⟩, kết quả là cos²(π/8), khoảng 0,854. Không kênh nào làm tăng khoảng cách vết. Và nếu hai mạch lệch nhau ε thì mọi xác suất đo lệch tối đa ε, nên T cổng mỗi cổng sai ε chỉ gây sai tối đa Tε. Đó là cách sai số đa thức của QSVT chuyển thành sai số của phép đo.

### Slide 13 — Section 02 Classic algorithms · 08:50 (10 s)

**EN:** Before QSVT, four classic algorithms that it will later absorb.

**VI:** Trước QSVT, bốn thuật toán gốc mà về sau QSVT sẽ bao trùm.

### Slide 14 — Four classic algorithms · 09:00 (90 s)

**EN:** Deutsch–Jozsa decides constant versus balanced with one query instead of 2 to the n minus 1 plus 1, thanks to phase kickback, which turns a bit oracle into a phase oracle. Grover is two reflections, so it is a rotation by 2 theta in a 2D plane; the best number of rounds is about pi over 4 times root N over M. The QFT is the normalised DFT, built from n times n plus 1 over 2 gates. Phase estimation finds the nearest value with probability at least 4 over pi squared, and run on the Grover operator it becomes amplitude estimation, with error about 1 over M. For data, that means estimating a mean with order 1 over epsilon queries instead of 1 over epsilon squared samples.

**VI:** Deutsch–Jozsa phân biệt hàm hằng với hàm cân bằng chỉ bằng một truy vấn thay vì 2^(n−1) + 1, nhờ phase kickback biến oracle bit thành oracle pha. Grover là tích hai phép phản xạ, nên là một phép quay góc 2θ trong mặt phẳng 2 chiều; số vòng tối ưu khoảng (π/4)√(N/M). QFT là DFT chuẩn hóa, dựng từ n(n+1)/2 cổng. Ước lượng pha tìm giá trị gần nhất với xác suất ít nhất 4/π², và khi chạy trên toán tử Grover thì thành amplitude estimation với sai số cỡ 1/M. Với dữ liệu, điều đó nghĩa là ước lượng trung bình bằng O(1/ε) truy vấn thay vì O(1/ε²) mẫu.

### Slide 15 — Grover is a 2D rotation · 10:30 (30 s) and 12:30 (30 s, handoff)

**EN:** Here is Grover for N equal to 64, with one and with three solutions. The dots are a statevector simulation, the lines are the formula sine squared of 2k plus 1 theta; they agree to 10⁻¹⁶. Past the best k, the probability falls: Grover overshoots. Let me run it. *(Demo 0.)* *(After the demo:)* So Grover is really a polynomial in disguise. [Speaker 2] will show why.

**VI:** Đây là Grover với N = 64, một nghiệm và ba nghiệm. Các chấm là mô phỏng statevector, đường liền là công thức sin²((2k+1)θ); hai bên khớp tới 10⁻¹⁶. Qua k tối ưu thì xác suất giảm: Grover quay quá. Mời xem chạy thử. *(Demo 0.)* *(Sau demo:)* Vậy Grover thật ra là một đa thức đội lốt. [Người nói 2] sẽ giải thích vì sao.

### ▶ Demo 0 — `demo0_foundations_grover.ipynb` · 11:00–12:30 (1 min 30 s)

1. *Cell 2, saved output (20 s).* **EN:** Helstrom, measured with the optimal projector: 0.8536, equal to cos² π/8. The Werner state's smallest partial-transpose eigenvalue changes sign at p equal to one third. Post-selection gives 0.13. All PASS. **VI:** Helstrom đo bằng projector tối ưu: 0,8536, đúng bằng cos²(π/8). Trị riêng nhỏ nhất của chuyển vị riêng phần của trạng thái Werner đổi dấu tại p = 1/3. Hậu chọn cho 0,13. Tất cả PASS.
2. *Run cell 3 (50 s).* **EN:** Grover on 64 items: the simulation matches the formula to 10⁻¹⁶, with k* equal to 6 for one solution and 3 for three. **VI:** Grover trên 64 phần tử: mô phỏng khớp công thức tới 10⁻¹⁶, k* = 6 với một nghiệm và 3 với ba nghiệm.
3. *Run cell 4 (20 s).* **EN:** On Aer, 20,000 shots at k* = 6: theory 0.9966, measured 0.9967, inside 3σ. **VI:** Trên Aer, 20.000 shot tại k* = 6: lý thuyết 0,9966, đo được 0,9967, nằm trong 3σ.

---

## Speaker 2 / Người nói 2 — QSP and QSVT (13:00–27:00)

### Slide 16 — Section 03 QSP and QSVT · 13:00 (10 s)

**EN:** Thank you. Why do rotations give polynomials, and why does that work for whole matrices?

**VI:** Cảm ơn. Vì sao các phép quay tạo ra đa thức, và vì sao điều đó đúng cho cả ma trận?

### Slide 17 — Two signal conventions · 13:10 (40 s)

**EN:** Two ways to write the signal. W of x, e to the i arc-cosine x X, is how the QSP theorem is stated, and zero phases give Chebyshev. R of x is a reflection, the form block-encodings use. They differ only by fixed Z rotations and a global phase. Mixing them up is the most common bug, so we put the convention in every function name.

**VI:** Có hai cách viết tín hiệu. W(x) = e^(i arccos(x) X) là dạng dùng để phát biểu định lý QSP, và pha 0 cho ra Chebyshev. R(x) là một phép phản xạ, dạng mà block-encoding dùng. Hai dạng chỉ khác nhau các phép quay Z cố định và một pha toàn cục. Lẫn hai quy ước là lỗi hay gặp nhất, nên nhóm ghi quy ước ngay trong tên mỗi hàm.

### Slide 18 — Phases are the dials · 13:50 (70 s)

**EN:** QSP alternates two kinds of single-qubit gates. The filled boxes are the signal, W of x, a rotation by arc-cosine x. The outlined boxes are phase rotations, and the phases are the dials we turn. The product is a 2×2 matrix whose top-left entry is a polynomial P of x. The QSP theorem says exactly which polynomials we can get: degree at most d, parity d mod 2, and a normalisation condition. The practical version: any real polynomial with the right parity and absolute value at most 1 can be made the real part of P. The phases are the dials; the polynomial is the output.

**VI:** QSP xen kẽ hai loại cổng một qubit. Ô đậm là tín hiệu W(x), một phép quay góc arccos x. Ô viền là phép quay pha, và các pha chính là núm vặn. Tích của chúng là ma trận 2×2 có phần tử trên-trái là một đa thức P(x). Định lý QSP nói chính xác đa thức nào đạt được: bậc tối đa d, chẵn lẻ theo d mod 2, và một điều kiện chuẩn hóa. Hệ quả thực hành: mọi đa thức thực đúng chẵn lẻ và có trị tuyệt đối không quá 1 đều làm được phần thực của P. Pha là núm vặn, đa thức là đầu ra.

### Slide 19 — Zero phases give Chebyshev · 15:00 (40 s)

**EN:** Here is the first test for any QSP implementation. Set every phase to zero, and P of x must be cos of d arc-cosine x, the Chebyshev polynomial T_d. Our code matches T_3, T_6 and T_9 with a largest error of 2.5 times 10⁻¹⁵. Before the demo, two practical questions: how high must the degree be, and how do we find the phases?

**VI:** Đây là phép thử đầu tiên cho mọi cài đặt QSP. Đặt mọi pha bằng 0 thì P(x) phải bằng cos(d·arccos x), tức đa thức Chebyshev T_d. Code của nhóm khớp T_3, T_6 và T_9 với sai số lớn nhất 2,5·10⁻¹⁵. Trước khi demo, còn hai câu hỏi thực tế: bậc phải cao đến đâu, và tìm pha bằng cách nào?

### Slide 20 — Degree follows smoothness · 15:40 (60 s)

**EN:** The degree is the number of queries, so it is the cost. Smooth targets are cheap: cos tx to 10⁻⁶ needs degree 6 to 48 for t from 1 to 32, about 1.5 t. Our smoothed 1 over x needs about 13 kappa. A step of width delta needs about 5 over delta. The rule: the steeper the function, the higher the degree, about 1 over delta times log 1 over epsilon. And one warning: Chebyshev interpolation can overshoot 1, so we always check the maximum on 4,001 points first.

**VI:** Bậc chính là số truy vấn, tức là chi phí. Hàm trơn thì rẻ: cos(tx) với sai số 10⁻⁶ cần bậc 6 đến 48 khi t từ 1 đến 32, khoảng 1,5t. Hàm 1/x làm trơn cần khoảng 13κ. Hàm bước rộng δ cần khoảng 5/δ. Quy luật: hàm càng dốc thì bậc càng cao, cỡ (1/δ)·log(1/ε). Và một cảnh báo: nội suy Chebyshev có thể vượt 1, nên nhóm luôn kiểm tra giá trị lớn nhất trên 4.001 điểm trước.

### Slide 21 — Five ways to find phases · 16:40 (40 s)

**EN:** Given the polynomial, the phases are computed classically. We wrote our own BFGS fit. The QSPPACK optimiser of Dong and colleagues reaches degrees above ten thousand. Haah's factorisation is exact but needs high precision. pyqsp lets us cross-check. And generalised QSP removes the parity constraint. Let's find phases live.

**VI:** Khi đã có đa thức, pha được tính bằng máy cổ điển. Nhóm tự viết BFGS. Bộ tối ưu QSPPACK của Dong và cộng sự xử lý được bậc trên 10.000. Phân tích nhân tử của Haah cho kết quả chính xác nhưng cần độ chính xác số cao. pyqsp dùng để đối chiếu. Còn GQSP bỏ được ràng buộc chẵn lẻ. Giờ mời xem tìm pha trực tiếp.

### ▶ Demo 1 — `demo1_qsp_phases.ipynb` · 17:20–19:20 (2 min)

*Shortened to 2 minutes: mention cell 1 while switching screens, run cells 2, 4 and 5, and only read the result of cell 3. / Rút còn 2 phút: nói cell 1 khi chuyển màn hình, chạy cell 2, 4, 5, cell 3 chỉ đọc kết quả.*

1. *Cell 1 (15 s).* **EN:** All functions live in `qsvt_demo.py`, with a fixed seed of 1234. **VI:** Toàn bộ hàm nằm trong `qsvt_demo.py`, seed cố định 1234.
2. *Run cell 2 (30 s).* **EN:** With zero phases, QSP gives Chebyshev exactly: three errors around 10⁻¹⁵, and PASS. **VI:** Không cần pha, QSP cho đúng Chebyshev: ba sai số cỡ 10⁻¹⁵ và PASS.
3. *Run cell 3 (20 s).* **EN:** This checks the R_Z sign convention before anything else. Error zero, PASS. **VI:** Ô này kiểm tra quy ước dấu R_Z trước mọi thứ khác. Sai số bằng 0, PASS.
4. *Run cell 4 (60 s).* **EN:** Now we find 11 phases for 0.8 cos 3x with our own BFGS, 8 random starts, fitted on Chebyshev nodes. It takes about five seconds. Max error 1.97 times 10⁻⁶, and the two curves overlap. **VI:** Giờ tìm 11 pha cho 0,8·cos(3x) bằng BFGS tự viết, 8 lần khởi tạo, khớp trên nút Chebyshev. Mất khoảng 5 giây. Sai số đều 1,97·10⁻⁶ và hai đường trùng nhau.
5. *Run cell 5 (25 s).* **EN:** Always check that the target stays within 1 before fitting. Here the max is 0.8, PASS. **VI:** Luôn kiểm tra hàm mục tiêu không vượt 1 trước khi tìm pha. Ở đây max là 0,8, PASS.

*If cell 4 takes more than 20 s, stop it and run cell 4b, which loads the saved phases. / Nếu cell 4 chạy quá 20 giây, dừng lại và chạy cell 4b để đọc pha đã lưu.*

### Slide 22 — Demo 1: finding phases · 19:20 (20 s)

**EN:** To sum up: 11 phases, five seconds, an error of 2 times 10⁻⁶. One qubit is done. Now, how do we apply the same phases to a whole matrix?

**VI:** Tóm lại: 11 pha, 5 giây, sai số 2·10⁻⁶. Một qubit đã xong. Giờ làm sao áp cùng bộ pha đó lên cả một ma trận?

### Slide 23 — Put A inside a unitary · 19:40 (80 s)

**EN:** A quantum computer can only apply unitaries, so we hide A inside a bigger one. For a Hermitian A with norm at most 1, the reflection block-encoding puts A in the top-left block, square root of I minus A squared off the diagonal, and minus A in the corner. This matrix is both unitary and Hermitian. When we measure the ancilla and get zero, we have applied A to psi, with probability norm of A psi squared, the formula from slide 7. For a general matrix written as a sum of unitaries, LCU does the same job: PREP dagger, SELECT, PREP block-encodes A over the 1-norm of the coefficients.

**VI:** Máy tính lượng tử chỉ áp được unitary, nên ta giấu A vào một unitary lớn hơn. Với A Hermitian có chuẩn không quá 1, block-encoding kiểu phản xạ đặt A ở khối trên-trái, căn của I trừ A bình phương ở hai khối chéo, và trừ A ở góc dưới. Ma trận này vừa unitary vừa Hermitian. Khi đo ancilla ra 0 là ta đã áp A lên psi, với xác suất bằng chuẩn của A psi bình phương, đúng công thức ở slide 7. Với ma trận tổng quát viết thành tổng các unitary, LCU làm việc tương tự: PREP chuyển vị liên hợp, SELECT, PREP sẽ block-encode A chia chuẩn 1 của hệ số.

### Slide 24 — Focus: RQ1 · 21:00 (20 s)

**EN:** Here is the answer to RQ1, the one idea to remember from my part. Each eigenvalue runs its own QSP, with the same phases. Put together, the top-left block is P of A.

**VI:** Đây là câu trả lời cho RQ1, ý duy nhất cần nhớ trong phần của tôi. Mỗi trị riêng chạy một bài QSP riêng, với cùng một bộ pha. Ghép lại, khối trên-trái chính là P(A).

### Slide 25 — One QSP per eigenvalue · 21:20 (90 s)

**EN:** Why does that work? Take an eigenvector v with eigenvalue lambda. The two-dimensional space spanned by zero-v and one-v is invariant: U_A never leaves it. Inside that space, U_A acts exactly like the 2×2 reflection R of lambda, and the projector-controlled phase acts like e to the i phi Z. So the whole sequence acts like a QSP sequence at x equal to lambda, and produces P of lambda. Every eigenvalue gets its own copy, in parallel, with the same phases. Summing over eigenvectors, the top-left block is the sum of P of lambda_k times v_k v_k dagger, which is P of A. For non-Hermitian matrices, the same argument works on singular values, through the cosine-sine decomposition.

**VI:** Vì sao được như vậy? Lấy một vector riêng v với trị riêng lambda. Không gian hai chiều sinh bởi |0⟩|v⟩ và |1⟩|v⟩ là bất biến: U_A không bao giờ đưa ra khỏi nó. Trong không gian đó, U_A tác động đúng như phép phản xạ 2×2 R(lambda), còn pha điều khiển bởi projector tác động như e mũ i phi Z. Vậy cả chuỗi tác động như một chuỗi QSP tại x = lambda và cho ra P(lambda). Mỗi trị riêng có một bản riêng, chạy song song, với cùng bộ pha. Cộng theo các vector riêng, khối trên-trái là tổng P(lambda_k) nhân v_k v_k chuyển vị liên hợp, tức là P(A). Với ma trận không Hermitian, lập luận tương tự áp dụng cho giá trị kỳ dị qua phân rã cosine–sine.

### Slide 26 — From formula to circuit · 22:50 (40 s)

**EN:** Four steps turn the formula into a circuit. With one ancilla, each phase is an R_Z on the ancilla. With several ancillas, we add one qubit, flip it with a multi-controlled NOT when all ancillas are zero, rotate it, and uncompute. We append gates in reverse. And to keep only the real part of P, we average the sequences with phi and minus phi by LCU, at the price of one more qubit and a lower success probability.

**VI:** Bốn bước biến công thức thành mạch. Với một ancilla, mỗi pha là một cổng R_Z trên ancilla. Với nhiều ancilla, thêm một qubit, lật nó bằng NOT đa điều khiển khi mọi ancilla bằng 0, quay nó, rồi uncompute. Cổng được append theo thứ tự đảo. Và để chỉ giữ phần thực của P, lấy trung bình hai chuỗi với φ và −φ bằng LCU, đổi lại tốn thêm một qubit và xác suất thành công thấp hơn.

### Slide 27 — The QSVT circuit in Qiskit · 23:30 (40 s)

**EN:** This is the real circuit: three qubits, with the ancilla on q2. With one ancilla, every phase is just an R_Z of minus two phi on the ancilla, and the light boxes are the 10 calls to U_A. We build it in reverse order, as slide 6 warned. The circuit's matrix matches the numpy matrix to 9.5 times 10⁻¹⁶. One honest note: measuring gives the complex P of A; to get only its real part you need one more qubit and an LCU step, which we do not use today. Let's run it.

**VI:** Đây là mạch thật: ba qubit, ancilla là q2. Với một ancilla, mỗi pha chỉ là một cổng R_Z(−2φ) trên ancilla, còn các ô sáng là 10 lần gọi U_A. Mạch được dựng theo thứ tự đảo, như slide 6 đã cảnh báo. Ma trận của mạch khớp ma trận numpy với sai số 9,5·10⁻¹⁶. Một lưu ý thẳng thắn: phép đo cho ra P(A) dạng phức; muốn lấy riêng phần thực cần thêm một qubit và một bước LCU, hôm nay nhóm không dùng bước đó. Giờ mời xem chạy thử.

### ▶ Demo 2 — `demo2_qsvt_circuit_measure.ipynb` · 24:10–26:40 (2 min 30 s)

1. *Cell 1 (20 s).* **EN:** A random symmetric 4×4 matrix, scaled so its norm is below 1. Four eigenvalues, all inside minus 1 to 1. **VI:** Ma trận đối xứng 4×4 ngẫu nhiên, chia để chuẩn nhỏ hơn 1. Bốn trị riêng đều nằm trong khoảng −1 đến 1.
2. *Run cell 2 (25 s).* **EN:** The block-encoding is an 8×8 unitary with A in the corner. Both errors are below 10⁻¹², PASS. **VI:** Block-encoding là unitary 8×8 với A ở góc. Hai sai số đều dưới 10⁻¹², PASS.
3. *Run cell 3 (35 s).* **EN:** This is RQ1 in numbers. For each eigenvalue, the 2×2 block equals R of lambda, and nothing leaks out of the subspace. **VI:** Đây là RQ1 bằng số. Với mỗi trị riêng, khối 2×2 bằng R(lambda), và không có gì rò ra khỏi không gian con.
4. *Run cell 4 (30 s).* **EN:** The same 11 phases from Demo 1, now applied to the whole matrix. The error against 0.8 cos 3A is 1.2 times 10⁻⁶, the same size as the fitting error. **VI:** Cùng 11 pha từ Demo 1, giờ áp lên cả ma trận. Sai số so với 0,8·cos(3A) là 1,2·10⁻⁶, cùng cỡ với sai số xấp xỉ.
5. *Run cell 5 (30 s).* **EN:** The circuit: 10 U_A calls, 11 R_Z gates, and it matches numpy to 10⁻¹⁵. **VI:** Mạch có 10 lần gọi U_A, 11 cổng R_Z, và khớp numpy tới 10⁻¹⁵.
6. *Run cell 6 (40 s).* **EN:** Now we measure the ancilla 20,000 times on Aer. Theory says 0.5217, we measure 0.5223, well inside the 3σ window of 0.0106. The post-selected state has fidelity 1. **VI:** Giờ đo ancilla 20.000 lần trên Aer. Lý thuyết là 0,5217, đo được 0,5223, nằm gọn trong khoảng 3σ = 0,0106. Trạng thái hậu chọn có fidelity bằng 1.

*If Aer is slow, show the saved output of cell 6 and read the three numbers. / Nếu Aer chậm, mở output đã lưu của cell 6 và đọc ba con số.*

### Slide 28 — Demo 2: measured QSVT · 26:40 (20 s, handoff)

**EN:** Five checks, five passes, from the block-encoding to the measurement. The framework works. Now we choose polynomials, first for three classic algorithms, then for big data. Over to [Speaker 3].

**VI:** Năm phép kiểm tra, cả năm đều đạt, từ block-encoding đến phép đo. Khung đã chạy. Giờ ta chọn đa thức, trước cho ba thuật toán kinh điển, sau đó cho dữ liệu lớn. Xin mời [Người nói 3].

---

## Speaker 3 / Người nói 3 — Algorithms, big data, conclusion (27:00–42:00)

### Slide 29 — Section 04 Algorithms · 27:00 (10 s)

**EN:** Thank you. Which polynomial solves which problem?

**VI:** Cảm ơn. Đa thức nào giải bài toán nào?

### Slide 30 — Fixed-point never overshoots · 27:10 (70 s)

**EN:** Start with search. Grover is QSP at x equal to square root of a, where a is the fraction of solutions, and its polynomial is T_{2k+1}. The grey curve shows the known weakness: if you do not know a, you overshoot, and the success probability swings down to zero. Yoder, Low and Chuang chose a different polynomial. With the same 7 oracle calls, the cyan curve stays above 0.99 for every a above 0.05, without knowing a. Change the polynomial, change the behaviour.

**VI:** Bắt đầu với tìm kiếm. Grover là QSP tại x bằng căn của a, với a là tỉ lệ nghiệm, và đa thức của nó là T_{2k+1}. Đường xám cho thấy điểm yếu quen thuộc: nếu không biết a thì sẽ quay quá, xác suất thành công rơi về 0. Yoder, Low và Chuang chọn một đa thức khác. Với cùng 7 lần gọi oracle, đường cyan luôn trên 0,99 với mọi a lớn hơn 0,05 mà không cần biết a. Đổi đa thức là đổi hành vi.

### Slide 31 — Hamiltonian simulation · 28:20 (70 s)

**EN:** Next, simulating e to the minus iHt. The Jacobi–Anger expansion writes cos tx and sin tx in Chebyshev polynomials, so the degree is order t plus log 1 over epsilon, which Low and Chuang proved optimal. We did this at the analysis level with numpy, not as a full circuit. For a random 8×8 Hamiltonian and an error of 10⁻³, at t equal to 32 QSVT needs 43 queries. First-order Trotter needs 12,525 steps, and second-order needs 742. One honest note: our first-order Trotter count grew almost linearly in t, slower than the t-squared worst-case bound.

**VI:** Tiếp theo là mô phỏng e mũ trừ iHt. Khai triển Jacobi–Anger viết cos(tx) và sin(tx) theo đa thức Chebyshev, nên bậc là O(t + log 1/ε), và Low–Chuang đã chứng minh mức này là tối ưu. Nhóm làm ở mức phân tích bằng numpy, chưa dựng mạch đầy đủ. Với Hamiltonian ngẫu nhiên 8×8 và sai số 10⁻³, tại t = 32 QSVT cần 43 truy vấn. Trotter bậc 1 cần 12.525 bước, bậc 2 cần 742. Một lưu ý thẳng thắn: số bước Trotter bậc 1 đo được tăng gần tuyến tính theo t, chậm hơn cận xấu nhất t bình phương.

### Slide 32 — Linear systems: degree vs κ · 29:30 (60 s)

**EN:** For linear systems, we approximate 1 over x, smoothed near zero, with an odd polynomial. The table shows the degree grows linearly in the condition number kappa, about 13.3 kappa, from 27 at kappa 2 to 427 at kappa 32. The solution error stays around 10⁻³. The success probability drops as kappa grows, down to 0.02, which is why a real solver adds amplitude amplification. Compared with HHL, QSVT needs only one or two ancillas and depends on log 1 over epsilon instead of a polynomial in 1 over epsilon.

**VI:** Với hệ tuyến tính, nhóm xấp xỉ 1/x, làm trơn gần 0, bằng một đa thức lẻ. Bảng cho thấy bậc tăng tuyến tính theo số điều kiện kappa, khoảng 13,3 kappa, từ 27 khi kappa = 2 đến 427 khi kappa = 32. Sai số nghiệm giữ quanh 10⁻³. Xác suất hậu chọn giảm khi kappa tăng, xuống 0,02, nên bộ giải thật cần thêm amplitude amplification. So với HHL, QSVT chỉ cần một đến hai ancilla và phụ thuộc log(1/ε) thay vì đa thức theo 1/ε.

### Slide 33 — Focus: a bug we really hit · 30:30 (15 s)

**EN:** One lesson from building this. Our first smoothed 1 over x went above 1, to about 1.91, and a function above 1 has no phases at all. Scaling by 0.5 fixed it. Always check the bound before you fit.

**VI:** Một bài học khi làm đề tài. Hàm 1/x làm trơn đầu tiên của nhóm vượt 1, khoảng 1,91, mà hàm vượt 1 thì không có bộ pha nào cả. Nhân 0,5 là sửa được. Luôn kiểm tra cận trước khi tìm pha.

### Slide 34 — Grover is optimal · 30:45 (45 s)

**EN:** QSVT tells us how to be fast. The polynomial method tells us we cannot be faster. After T queries, every success probability is a polynomial of degree at most 2T. So the number of queries is at least half the minimum degree that approximates the function. For OR on N bits, our linear program finds degrees 3, 6 and 11, so d over square root of N stays near 0.7. OR needs order square root N queries, and Grover is optimal.

**VI:** QSVT cho biết cách làm nhanh. Polynomial method cho biết không thể nhanh hơn. Sau T truy vấn, mọi xác suất thành công là đa thức bậc tối đa 2T. Vì vậy số truy vấn ít nhất bằng một nửa bậc nhỏ nhất xấp xỉ được hàm. Với hàm OR trên N bit, quy hoạch tuyến tính của nhóm tìm ra bậc 3, 6 và 11, nên d chia căn N giữ quanh 0,7. OR cần cỡ căn N truy vấn, và Grover là tối ưu.

### Slide 35 — One table, five results · 31:30 (30 s)

**EN:** Everything so far in one table: one circuit, five polynomials. The new row, the eigenvalue filter, is a smoothed step function. It replaces phase estimation, and it leads straight into big data: it is how we will do PCA.

**VI:** Toàn bộ kết quả đến giờ trong một bảng: một mạch, năm đa thức. Hàng mới, bộ lọc trị riêng, là một hàm bước làm trơn. Nó thay cho ước lượng pha, và dẫn thẳng sang dữ liệu lớn: đây chính là cách làm PCA.

### Slide 36 — Section 05 Big Data · 32:00 (10 s)

**EN:** Now back to the 10¹²-entry matrix from the start.

**VI:** Giờ quay lại ma trận 10¹² ô ở đầu bài.

### Slide 37 — Big data through QSVT · 32:10 (60 s)

**EN:** Each data task becomes a polynomial. Search uses Chebyshev or fixed-point polynomials, root N instead of N. Estimating a mean uses amplitude estimation, 1 over epsilon instead of 1 over epsilon squared samples. Regression applies a smoothed 1 over x to the singular values, with cost growing with kappa. PCA applies a smoothed step, with cost growing as the gap shrinks. Recommendation samples from a filtered low-rank matrix; with QRAM that is polylog in the matrix size, but as we will see, so is the classical answer.

**VI:** Mỗi bài toán dữ liệu trở thành một đa thức. Tìm kiếm dùng đa thức Chebyshev hoặc fixed-point, căn N thay vì N. Ước lượng trung bình dùng amplitude estimation, 1/ε thay vì 1/ε² mẫu. Hồi quy áp 1/x làm trơn lên giá trị kỳ dị, chi phí tăng theo κ. PCA áp hàm bước làm trơn, chi phí tăng khi khe hở hẹp lại. Khuyến nghị lấy mẫu từ ma trận hạng thấp đã lọc; với QRAM chi phí là polylog theo kích thước, nhưng như ta sẽ thấy, phía cổ điển cũng vậy.

### Slide 38 — Regression with QSVT · 33:10 (60 s)

**EN:** Regression in practice. The data matrix X is 12 samples by 4 features, not square, so we embed it in the Hermitian matrix with X and X-transpose off the diagonal. Its eigenvalues are plus and minus the singular values of X. Applying our smoothed 1 over x, an odd function that is zero at zero, gives X-plus y in the lower block. The 16×16 matrix needs 4 qubits plus 1 ancilla. At kappa 4 the degree is 53, and beta matches numpy's least squares to 2 times 10⁻³.

**VI:** Hồi quy trong thực tế. Ma trận dữ liệu X có 12 mẫu, 4 đặc trưng, không vuông, nên nhóm nhúng nó vào ma trận Hermitian có X và Xᵀ ở hai khối chéo. Trị riêng của ma trận này là cộng trừ các giá trị kỳ dị của X. Áp hàm 1/x làm trơn, một hàm lẻ bằng 0 tại 0, cho ra X⁺y ở khối dưới. Ma trận 16×16 cần 4 qubit cộng 1 ancilla. Với κ = 4 bậc là 53, và β khớp với least squares của numpy tới 2·10⁻³.

### Slide 39 — PCA by filtering σ · 34:10 (60 s)

**EN:** PCA in practice. This 16×16 matrix has two strong components and noise below 0.25. An even polynomial that approximates a step at 0.5 keeps the two components and drops the noise, with a projector error of 4 times 10⁻³. The cost depends on the gap between signal and noise: the degree is about 5 over delta, from 16 to 95 as the gap shrinks from 0.3 to 0.05. This filter is also the core of quantum recommendation systems. Let's run both.

**VI:** PCA trong thực tế. Ma trận 16×16 này có hai thành phần mạnh và nhiễu dưới 0,25. Một đa thức chẵn xấp xỉ hàm bước tại 0,5 giữ lại hai thành phần và bỏ nhiễu, với sai số projector 4·10⁻³. Chi phí phụ thuộc khe hở giữa tín hiệu và nhiễu: bậc khoảng 5/δ, từ 16 lên 95 khi khe hở hẹp từ 0,3 xuống 0,05. Bộ lọc này cũng là lõi của hệ khuyến nghị lượng tử. Mời xem chạy cả hai.

### ▶ Demo 4 — `demo4_bigdata.ipynb` · 35:10–37:10 (2 min)

1. *Run cell 2 (50 s).* **EN:** Regression: degree 53, and the two beta vectors agree to about 2 times 10⁻³. Success probability is only 0.03, which is why real solvers add amplitude amplification. **VI:** Hồi quy: bậc 53, hai vector β khớp nhau cỡ 2·10⁻³. Xác suất hậu chọn chỉ 0,03, nên bộ giải thật cần thêm amplitude amplification.
2. *Run cell 3 (40 s).* **EN:** PCA: degrees 16, 26, 50, 95, and degree times delta stays near 5. **VI:** PCA: bậc 16, 26, 50, 95, và bậc nhân δ giữ quanh 5.
3. *Run cell 4 (30 s).* **EN:** And the catch: for a random full-rank 1024×1024 matrix, the Frobenius norm is 16 times the spectral norm; for rank 5 it is about 2. Keep that 16 in mind. **VI:** Và cái bẫy: với ma trận ngẫu nhiên đầy đủ hạng 1024×1024, chuẩn Frobenius gấp 16 lần chuẩn phổ; với hạng 5 chỉ khoảng 2. Hãy nhớ con số 16 này.

*If the machine is slow, run cell 5, which reads the saved results. / Nếu máy chậm, chạy cell 5 để đọc kết quả đã lưu.*

### Slide 40 — Focus: the catch · 37:10 (20 s)

**EN:** Here is the catch. QSVT counts queries to the block-encoding. It does not count the cost of building it. So how does big data get in, and how do the answers get out?

**VI:** Đây là cái bẫy. QSVT đếm số truy vấn tới block-encoding. Nó không đếm chi phí dựng block-encoding. Vậy dữ liệu lớn vào máy bằng cách nào, và kết quả ra bằng cách nào?

### Slide 41 — Three traps for big data · 37:30 (70 s)

**EN:** Three traps. Loading: a block-encoding built from classical data through QRAM is normalised by the Frobenius norm, not the spectral norm, so every query count is multiplied by their ratio, 16 for our random 1024×1024 matrix, and large QRAM does not exist yet. Reading out: the answer is a quantum state, and reading all N entries takes at least N runs. Dequantization: Ewin Tang showed in 2018 that if the classical computer gets the same sampling access, it can match the low-rank speedups, as the seminar's Part 3 also mentioned.

**VI:** Ba cái bẫy. Nạp dữ liệu: block-encoding dựng từ dữ liệu cổ điển qua QRAM bị chuẩn hóa bởi chuẩn Frobenius chứ không phải chuẩn phổ, nên mọi số truy vấn bị nhân với tỉ lệ đó, bằng 16 với ma trận ngẫu nhiên 1024×1024 của nhóm, và QRAM lớn hiện chưa tồn tại. Đọc kết quả: đáp án là một trạng thái lượng tử, đọc đủ N phần tử cần ít nhất N lần chạy. Dequantization: năm 2018 Ewin Tang chỉ ra rằng nếu máy cổ điển có cùng kiểu truy cập lấy mẫu, nó cũng đạt được tăng tốc cho ma trận hạng thấp, như Phần 3 của seminar đã nhắc.

### Slide 42 — Who wins, and when · 38:40 (50 s)

**EN:** Putting costs side by side. Classical regression costs n d squared and returns the full vector. QSVT with QRAM costs about kappa-F log 1 over epsilon, where kappa-F uses the Frobenius norm, and returns only a state. Dequantized methods are polynomial in the rank, kappa and 1 over epsilon. For recommendation, both quantum and dequantized are polylog in the matrix size; the classical one has a much higher polynomial in k and 1 over epsilon, so a polynomial gap may remain, not an exponential one.

**VI:** Đặt chi phí cạnh nhau. Hồi quy cổ điển tốn O(nd²) và trả về cả vector. QSVT với QRAM tốn khoảng κ_F·log(1/ε), trong đó κ_F dùng chuẩn Frobenius, và chỉ trả về một trạng thái. Phương pháp dequantized là đa thức theo hạng, κ và 1/ε. Với khuyến nghị, cả lượng tử lẫn dequantized đều polylog theo kích thước ma trận; bản cổ điển có đa thức bậc cao hơn nhiều theo k và 1/ε, nên khoảng cách có thể còn ở mức đa thức, không phải lũy thừa.

### Slide 43 — When QSVT might pay off · 39:30 (50 s)

**EN:** So when might QSVT pay off for data? When the data comes from a quantum process, so nothing needs loading. When the matrix is sparse or given by a formula, so a circuit builds the block-encoding without QRAM. When we only need a summary value, not the whole vector. When the matrix has high rank and small kappa, where dequantization fails. And on fault-tolerant hardware, after a resource estimate, for example with Qualtran.

**VI:** Vậy khi nào QSVT có thể đáng dùng cho dữ liệu? Khi dữ liệu đến từ một quá trình lượng tử nên không cần nạp. Khi ma trận thưa hoặc cho bằng công thức, nên dựng block-encoding bằng mạch mà không cần QRAM. Khi chỉ cần một đại lượng tóm tắt chứ không cần cả vector. Khi ma trận hạng cao và κ nhỏ, nơi dequantization không áp dụng được. Và trên phần cứng chịu lỗi, sau khi đã ước lượng tài nguyên, ví dụ bằng Qualtran.

### Slide 44 — Five questions, answered · 40:20 (40 s)

**EN:** Our answers. RQ0: QSVT trains linear algebra; measurement, mixed states and noise must be added. RQ1: each eigenvalue has its own invariant 2D subspace. RQ2: the degrees are 1 over root a, t plus log 1 over epsilon, and kappa log kappa over epsilon, and the polynomial method shows they are optimal. RQ3: 43 queries against 12,525 Trotter steps, with no phase estimation. RQ4: QSVT solves regression and PCA, but loading and reading the data decide whether there is a real speedup.

**VI:** Câu trả lời của nhóm. RQ0: QSVT luyện đại số tuyến tính; cần bổ sung đo lường, trạng thái hỗn hợp và nhiễu. RQ1: mỗi trị riêng có một không gian con 2 chiều bất biến riêng. RQ2: bậc lần lượt là 1/√a, t + log(1/ε) và κ log(κ/ε), và polynomial method cho thấy chúng tối ưu. RQ3: 43 truy vấn so với 12.525 bước Trotter, không cần ước lượng pha. RQ4: QSVT giải được hồi quy và PCA, nhưng việc nạp và đọc dữ liệu quyết định có tăng tốc thật hay không.

### Slide 45 — Limits and next steps · 41:00 (30 s)

**EN:** Our limits: simulator only, with QSVT matrices up to 16×16; Hamiltonian simulation and linear systems stop at degree analysis; and our big-data tests use small synthetic matrices. Next: full LCU circuits, transpiling to real devices, and noise.

**VI:** Giới hạn của đề tài: chỉ chạy simulator, ma trận QSVT tối đa 16×16; mô phỏng Hamiltonian và hệ tuyến tính dừng ở phân tích bậc; và các thử nghiệm Big Data dùng ma trận nhỏ, tổng hợp. Bước tiếp theo: mạch LCU đầy đủ, transpile lên thiết bị thật và mô phỏng nhiễu.

### Slide 46 — References · 41:30 (20 s)

**EN:** These are our main sources: the QSVT papers on the top line, and the big-data and dequantization papers below.

**VI:** Đây là các tài liệu chính: dòng trên là các bài về QSVT, dòng dưới là các bài về dữ liệu lớn và dequantization.

### Slide 47 — Thank you · 41:50

**EN:** Thank you. The code and the five notebooks are in the repository on screen. We are happy to take your questions.

**VI:** Xin cảm ơn. Code và năm notebook nằm trong repo trên màn hình. Nhóm xin nhận câu hỏi từ thầy cô và các bạn.

---

## Backup / Dự phòng: Demo 3 — `demo3_algorithms.ipynb`

*Not run live in the 45-minute version; open it only if asked about E4–E8. / Không chạy trực tiếp trong bản 45 phút; chỉ mở khi được hỏi về E4–E8.*

*Cells 1, 2 and 4 show saved outputs; only cell 3 runs live. / Cell 1, 2, 4 chỉ hiện output đã lưu; chỉ cell 3 chạy trực tiếp.*

1. *Cell 1 (40 s).* **EN:** This is slide 19 straight from the data: Grover oscillates, fixed-point stays above the dashed line, PASS. **VI:** Đây là slide 19 lấy trực tiếp từ dữ liệu: Grover dao động, fixed-point nằm trên đường nét đứt, PASS.
2. *Cell 2 (40 s).* **EN:** The full table behind slide 20: QSVT goes from 5 to 43, Trotter from 274 to 12,525. **VI:** Bảng đầy đủ phía sau slide 20: QSVT từ 5 lên 43, Trotter từ 274 lên 12.525.
3. *Run cell 3 (45 s).* **EN:** Watch this one. Without the 0.5 factor, our smoothed 1 over x reaches 1.914, and the check says FAIL. With the factor, 0.957, PASS. Then the degrees: 27, 53, 107, 213, about 13 per unit of kappa. **VI:** Chú ý ô này. Không có hệ số 0,5, hàm 1/x làm trơn đạt 1,914 và kiểm tra báo FAIL. Có hệ số thì còn 0,957, PASS. Sau đó là bậc: 27, 53, 107, 213, khoảng 13 cho mỗi đơn vị kappa.
4. *Cell 4 (25 s).* **EN:** The polynomial method: minimum degrees 3, 6 and 11 for N equal to 16, 64 and 256. **VI:** Polynomial method: bậc nhỏ nhất 3, 6 và 11 với N = 16, 64 và 256.

---

## Q&A / Hỏi đáp

Each answer ≤ 45 s. The owner answers first; the others add only if asked. / Mỗi câu trả lời tối đa 45 giây. Người phụ trách trả lời trước; người khác chỉ bổ sung khi được hỏi.

**Q: Is QSVT faster than classical computing? / QSVT có nhanh hơn máy tính cổ điển không?** — Speaker 3 / Người nói 3, slides 42–45

- **EN:** In queries to the block-encoding, yes, and the dependence on t, kappa and epsilon is optimal. End to end, it also depends on building the block-encoding, preparing the state and reading the result. Dequantization shows that for low-rank matrices with sampling access, classical methods can catch up.
- **VI:** Tính theo số truy vấn tới block-encoding thì có, và tối ưu theo t, κ, ε. Nhưng lợi thế end-to-end còn phụ thuộc chi phí dựng block-encoding, chuẩn bị trạng thái và đọc kết quả. Dequantization cho thấy với ma trận hạng thấp và truy cập lấy mẫu, máy cổ điển có thể bắt kịp.

**Q: Why only small matrices? / Vì sao chỉ thử ma trận nhỏ?** — Speaker 2 / Người nói 2, `E2_qsvt_matrices.ipynb`

- **EN:** A statevector needs 2ⁿ memory. Our goal is to verify the math, not to show speed, and the polynomial degree does not depend on the matrix size.
- **VI:** Mô phỏng statevector tốn bộ nhớ 2ⁿ. Mục tiêu là kiểm chứng toán, không phải chứng minh tốc độ, và bậc đa thức không phụ thuộc kích thước ma trận.

**Q: Did you run on real hardware? / Có chạy trên phần cứng thật không?** — Speaker 2 / Người nói 2

- **EN:** No. IBM sign-up is blocked from Vietnam. The optional experiment E9 transpiles to a fake backend to count CNOTs and depth, and simulates noise.
- **VI:** Không. Đăng ký IBM bị chặn từ Việt Nam. Thí nghiệm tùy chọn E9 transpile lên fake backend để đếm CNOT, độ sâu và mô phỏng nhiễu.

**Q: How is this different from HHL? / Khác HHL ở đâu?** — Speaker 3 / Người nói 3, slide 32

- **EN:** HHL uses phase estimation, so it depends polynomially on 1 over epsilon and needs a multi-qubit phase register. QSVT needs one or two ancillas and depends on log 1 over epsilon.
- **VI:** HHL dùng ước lượng pha nên phụ thuộc đa thức theo 1/ε và cần thanh ghi pha nhiều qubit. QSVT chỉ cần một đến hai ancilla và phụ thuộc log(1/ε).

**Q: Where do the phases come from? / Góc pha lấy từ đâu?** — Speaker 2 / Người nói 2, slide 21, Demo 1 cell 4

- **EN:** They are computed classically before running: pick the polynomial, check that it stays within 1, then find the phases by optimisation or factorisation. We wrote our own BFGS and can cross-check with pyqsp.
- **VI:** Tính bằng máy cổ điển trước khi chạy: chọn đa thức, kiểm tra không vượt 1, rồi tìm pha bằng tối ưu hóa hoặc phân tích nhân tử. Nhóm tự viết BFGS và có thể đối chiếu với pyqsp.

**Q: Why does a QSVT project include foundations? / Vì sao đề tài QSVT lại có phần toán nền?** — Speaker 1 / Người nói 1, slide 7

- **EN:** QSVT never uses measurement theory, density matrices, channels or trace distance. Stage 0 adds them, and A8 is also needed to turn a polynomial error into an error in measured probabilities.
- **VI:** QSVT không dùng lý thuyết đo lường, ma trận mật độ, kênh hay trace distance. Giai đoạn 0 bổ sung các phần này; riêng A8 còn cần để chuyển sai số của đa thức thành sai số xác suất đo.

**Q: What if phase finding does not converge? / Tìm pha không hội tụ thì sao?** — Speaker 2 / Người nói 2

- **EN:** Use more random starts, start from (π/4, 0, …, 0, π/4) as in Dong et al., lower the degree, or scale the target down a little.
- **VI:** Tăng số lần khởi tạo ngẫu nhiên, khởi tạo (π/4, 0, …, 0, π/4) theo Dong et al., giảm bậc hoặc co hàm mục tiêu nhỏ lại một chút.

**Q: Why is Grover optimal? / Vì sao Grover tối ưu?** — Speaker 3 / Người nói 3, slide 34

- **EN:** By the polynomial method: after T queries the success probability is a polynomial of degree at most 2T, and approximating OR on N bits needs degree order square root N.
- **VI:** Theo polynomial method: sau T truy vấn, xác suất thành công là đa thức bậc tối đa 2T, mà xấp xỉ hàm OR trên N bit cần bậc cỡ căn N.

**Q: Why did Trotter grow almost linearly in your data? / Vì sao Trotter trong dữ liệu tăng gần tuyến tính?** — Speaker 3 / Người nói 3, slide 31

- **EN:** The t-squared count is a worst-case bound. Our likely explanation is that, for this random 8×8 matrix, the step errors partly cancel instead of adding up; we have not proved it. QSVT still needs about 290 times fewer queries at t equal to 32.
- **VI:** Số bước t bình phương là cận trường hợp xấu nhất. Cách giải thích nhóm cho là hợp lý nhất: với ma trận 8×8 ngẫu nhiên này, sai số từng bước triệt tiêu một phần thay vì cộng dồn; nhóm chưa chứng minh điều này. QSVT vẫn cần ít hơn khoảng 290 lần ở t = 32.

**Q: Why not run on truly big data? / Vì sao không chạy trên dữ liệu thật lớn?** — Speaker 3 / Người nói 3

- **EN:** A statevector needs 2ⁿ memory, and our goal is to check the math. The degree depends on κ and the gap, not on the matrix size, so small matrices already show the cost.
- **VI:** Statevector tốn bộ nhớ 2ⁿ, và mục tiêu của nhóm là kiểm chứng toán. Bậc phụ thuộc κ và khe hở, không phụ thuộc kích thước ma trận, nên ma trận nhỏ đã cho thấy chi phí.

**Q: Does QRAM exist? / QRAM đã có chưa?** — Speaker 3 / Người nói 3, slide 41

- **EN:** Not at a useful size with error tolerance. That is the first trap on slide 41.
- **VI:** Chưa có QRAM đủ lớn và chịu được nhiễu. Đó là cái bẫy thứ nhất ở slide 41.

**Q: How does this compare with Spark or GPUs? / So với Spark hay GPU thì sao?** — Speaker 3 / Người nói 3, slides 42–43

- **EN:** Classical systems work on data already on disk. QSVT could only help when getting data in and out is cheap and a summary value is enough. Today, classical tools are the right choice.
- **VI:** Hệ cổ điển xử lý dữ liệu đã nằm sẵn trên đĩa. QSVT chỉ có thể giúp khi nạp và đọc dữ liệu rẻ và chỉ cần một đại lượng tóm tắt. Hiện tại nên dùng công cụ cổ điển.
