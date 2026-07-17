from tabulate import tabulate


class LibraryBorrow:
    def __init__(
        self, id, reader_name, book_name, borrow_days, late_days, fine_per_day
    ):
        self.id = id
        self.reader_name = reader_name
        self.book_name = book_name
        self.borrow_days = borrow_days
        self.late_days = late_days
        self.fine_per_day = fine_per_day

        self.total_fine = self.calculate_fine()
        self.fine_type = self.classify_fine()

    def calculate_fine(self):
        fine = self.late_days * self.fine_per_days

        return 0 if self.late_days == 0 else fine

    def classify_fine(self):
        if self.total_fine == 0:
            return "Không phạt"
        elif self.total_fine < 50000:
            return "Nhẹ"
        elif self.total_fine < 200000:
            return "Trung bình"
        else:
            return "Nặng"


# HÀM HELPER
def string_input(msg: str):
    while True:
        string = input(msg).strip()

        if string:
            return string
        print("Dữ liệu không được để trống")


def borrow_days_input():
    while True:
        try:
            val = int(input("Nhập số ngày mượn: "))
            if 1 <= val <= 365:
                return val
            print("Số ngày đã mượn phải là số nguyên từ 1 đến 365")
        except ValueError:
            print("Dữ liệu không hợp lệ")


def late_days_input(borrow_days):
    while True:
        try:
            val = int(input("Nhập số ngày muộn: "))

            if 0 <= val <= 365 and val <= borrow_days:
                return val
            print(
                "Số ngày trễ hạn phải là số nguyên từ 0 đến 365 và không được lớn hơn số ngày mượn"
            )
        except ValueError:
            print("Dữ liệu không hợp lệ")


def fine_input():
    while True:
        try:
            val = int(input("Nhập tiền phạt mỗi ngày trễ: "))

            if val >= 0:
                return val
            print("Tiền phạt mỗi ngày phải lớn hơn hoặc bằng 0")
        except ValueError:
            print("Dữ liệu không hợp lệ")


def search_results(data):
    if not data:
        print("Không tìm thấy")
    else:
        print("\n=== KẾT QUẢ TÌM KIẾM ===")
        for borrow in data:
            print(f"{borrow.reader_name} - {borrow.book_name}")


class LibraryBorrowManager:
    def __init__(self):
        self.borrow_records = []

    def _find_borrow_by_id(self, b_id: str):
        return next(
            (borrow for borrow in self.borrow_records if b_id == borrow.id), None
        )

    def add_borrow_record(self):
        print("\n=== THÊM PHIẾU MƯỢN ===")
        while True:
            b_id = string_input("Nhập ID phiếu mượn: ").strip().upper()

            if self._find_borrow_by_id(b_id):
                print("Phiếu mượn đã tồn tại")
            else:
                break
        b_name = string_input("Nhập tên người mượn: ").strip().title()
        book_name = string_input("Nhập tên sách: ").strip().capitalize()
        borrow_days = borrow_days_input()
        late_days = late_days_input(borrow_days)
        fine_days = fine_input()

        self.borrow_records.append(
            LibraryBorrow(b_id, b_name, book_name, borrow_days, late_days, fine_days)
        )
        print("Thêm phiếu thành công")

    def show_all(self):
        if not self.borrow_records:
            print("Danh sách hiện đang trống")
            return

        data = [
            [
                b.id,
                b.reader_name,
                b.book_name,
                b.borrow_days,
                b.late_days,
                f"{b.fine_per_days:,}",
                f"{b.total_fine:,}",
                b.fine_type,
            ]
            for b in self.borrow_records
        ]

        table = tabulate(
            data,
            headers=[
                "Mã Phiếu",
                "Họ tên bạn đọc",
                "Tên Sách",
                "Số ngày mượn",
                "Số ngày trễ hạn",
                "Tiền phạt mỗi ngày",
                "Tổng tiền phạt",
                "Phân loại mức phạt",
            ],
            tablefmt="grid",
        )
        print("\n==== DANH SÁCH PHIẾU MƯỢN ====")
        print(table)

    def update_borrow_record(self):
        print("\n==== UPDATE PHIẾU MƯỢN ====")
        update_id = string_input("Nhập ID phiếu muốn cập nhập: ").title().upper()

        borrow = self._find_borrow_by_id(update_id)

        if not borrow:
            print("Không tìm thấy phiếu")
            return

        borrow.borrow_days = borrow_days_input()
        borrow.late_days = late_days_input(borrow.borrow_days)
        borrow.fine_per_day = fine_input()
        borrow.total_fine = borrow.calculate_fine()
        borrow.fine_type = borrow.classify_fine()

        print("Cập nhập thành công")

    def delete_borrow_record(self):
        print("\n==== DELETE PHIẾU MƯỢN ====")
        delete_id = string_input("Nhập ID phiếu muốn cập nhập: ").title().upper()

        borrow = self._find_borrow_by_id(delete_id)

        if not borrow:
            print("Không tìm thấy phiếu")
            return

        confirm = input("Bạn có chắc muốn xóa phiếu này không? (Y/N): ").lower().strip()

        if confirm == "y":
            self.borrow_records.remove(borrow)
            print("Xóa phiếu mượn thành công!")
        elif confirm == "n":
            print("Đã hủy thao tác xóa!")
        else:
            print("Lựa chọn không hợp lệ")

    def search_borrow_record(self):
        print("\n=== TÌM KIẾM PHIẾU MƯỢN ====")
        print("1. Tìm theo tên bạn đọc")
        print("2. Tìm theo tên sách")
        choice = input("Lựa chọn của bạn là: ").strip()

        if choice == "1":
            reader_name = string_input("Nhập tên bạn đọc: ").strip().lower()

            data = [
                borrow
                for borrow in self.borrow_records
                if reader_name in borrow.reader_name.lower()
            ]
            search_results(data)

        elif choice == "2":
            book_name = string_input("Nhập tên sách: ").strip().lower()

            data = [
                borrow
                for borrow in self.borrow_records
                if book_name in borrow.book_name.lower()
            ]
            search_results(data)

        else:
            print("Lựa chọn không hợp lệ")

    def run(self):
        while True:
            choice = input("""\n================ MENU ================
1. Hiển thị danh sách phiếu mượn
2. Thêm phiếu mượn mới
3. Cập nhật phiếu mượn
4. Xóa phiếu mượn
5. Tìm kiếm phiếu mượn
6. Thoát
=====================================
Nhập lựa chọn của bạn: """).strip()

            match choice:
                case "1":
                    self.show_all()

                case "2":
                    self.add_borrow_record()

                case "3":
                    self.update_borrow_record()

                case "4":
                    self.delete_borrow_record()

                case "5":
                    self.search_borrow_record()

                case "6":
                    print("Đang thoát chương trình")
                    break

                case _:
                    print("Lựa chọn không hợp lệ")


def main():
    manager = LibraryBorrowManager()
    manager.run()


if __name__ == "__main__":
    main()
