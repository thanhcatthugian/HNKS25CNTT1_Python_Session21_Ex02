import logging

logging.basicConfig(
    filename="hl_menu_manager.log",
    level= logging.INFO,
    format="%(asctime)s -  %(levelname)s - %(message)s",

)

hl_menu_manager = logging.getLogger()

DRINK_MENU = {
"P1": {"name": "Phin Sữa Đá", "price": 35000},
"F1": {"name": "Freeze Trà Xanh", "price": 55000},
"T1": {"name": "Trà Sen Vàng", "price": 45000}
} 

current_order = [] 

def view_menu(menu):
    print("--- THỰC ĐƠN HIGHLANDS COFFEE ---")
    for i in menu:
        print(f"[{i}] - {menu[i]["name"]} - {menu[i]["price"]:,} VNĐ")
    hl_menu_manager.info("User viewed the menu")

def high_quant(quantity):
    if quantity <= 0:
        print("Số lượng phải lớn hơn 0!")
        hl_menu_manager.warning(f"InvalidQuantityError - Quantity: {quantity}")
        return "InvalidQuantityError"

def add_order(menu):
    print("--- THÊM MÓN VÀO GIỎ ---")
    while True:
        found = False
        new_id = input("Nhập mã đồ uống: ").strip().upper()
        if new_id == "":
            print("Không để trống mã đồ uống")
        else:
            for i in menu:
                if i == new_id:
                    found = True
                    while True:
                        try:
                            new_quantity = int(input("Nhập số lượng: "))
                        except ValueError:
                            print("Số lượng cần phải là một số nguyên lớn hơn 0")
                            hl_menu_manager.error("ValueError - Invalid quantity input")
                        else:
                            if new_quantity <= 0:
                                print("Số lượng phải lớn hơn 0!")
                                hl_menu_manager.warning(f"InvalidQuantityError - Quantity: {new_quantity}")
                            else:
                                current_order.append(
                                    {
                                        "drink_id": new_id,
                                        "name": menu[i]["name"],
                                        "price": menu[i]["price"],
                                        "quantity": new_quantity
                                    }
                                )
                                hl_menu_manager.info(f"Added {new_quantity} of {new_id} to order")
                                print(f"Đã thêm {new_quantity} x {menu[i]["name"]} vào giỏ hàng.")
                                break
            if not found:
                print("Mã đồ uống không hợp lệ, vui lòng kiểm tra lại thực đơn!")
                hl_menu_manager.warning(f"ItemNotFoundError - Code: {new_id}")
            else:
                break

def view_order_and_calc_total(orders):
    global total
    total = 0
    print("--- GIỎ HÀNG HIỆN TẠI ---\n"
          "Mã SP | Tên đồ uống          | Đơn giá  | Số lượng | Thành tiền\n"
          "----------------------------------------------------------------\n"
          )
    for i in orders:
        total+=i["quantity"]*i["price"]
        print(f"{i["drink_id"]}    | {i["name"]}          | {i["price"]:,}   | {i["quantity"]}        | {i["price"] * i["quantity"]:,} VNĐ")
    print("----------------------------------------------------------------\n"
          f"Tổng tiền cần thanh toán: {total:,} VNĐ"
          )

    hl_menu_manager.info("User viewed their order")
    return total

def pay_bill_and_delete_order(orders):
    print("--- THANH TOÁN ---")
    print(f"Tổng tiền cần thanh toán: {total:,} VNĐ")
    while True: 
        confirm = input(f"Xác nhận thanh toán {total:,} VNĐ? (y/n): ").strip().lower()
        if confirm == "":
            print("Không để trống lựa chọn xác nhận")
        elif confirm == "y":
            print("Thanh toán thành công.")
            hl_menu_manager.info("Checkout successful")
            for i in orders:
                orders.pop(orders.index(i))
            print("Giỏ hàng đã được làm trống.")
            break
        elif confirm =="n":
            print("Đã hủy thao tác thanh toán. Quay lại menu chính.")
            break
        else:
            print("Lựa chọn không hợp lệ. Thanh toán đã bị hủy.")
            break
if __name__ == "__main__":
    while True:
        try:
            decision = int(input("""========== HIGHLANDS MINI POS ==========
    1. Xem thực đơn
    2. Thêm món vào giỏ
    3. Xem giỏ hàng & Tính tổng tiền
    4. Thanh toán & Xóa giỏ hàng
    5. Thoát ca làm việc
    ========================================
    Chọn chức năng (1-5): """))
        except ValueError:
            print("Lựa chọn không hợp lệ, chỉ chọn 1- 5")
        else:
            match decision:
                case 1:
                    view_menu(DRINK_MENU)
                case 2:
                    add_order(DRINK_MENU)
                case 3:
                    if len(current_order)<=0:
                        print("Giỏ hàng trống, vui lòng chọn món (Chức năng 2).")
                    else:
                        view_order_and_calc_total(current_order)
                case 4:
                    if len(current_order)<=0:
                        print("Giỏ hàng trống, vui lòng chọn món (Chức năng 2).")
                    else:
                        pay_bill_and_delete_order(current_order)
                case 5:
                    print("Đã thoát ca làm việc. Hẹn gặp lại! ")
                    hl_menu_manager.info("Cashier logged out. System shutdown.")
                    break
                case _:
                    print("Lựa chọn không hợp lệ, chỉ chọn 1- 5")


'''
    Trả lời các bẫy dữ liệu đề đưa ra
    Bẫy 1 — Lỗi nhập chữ thay vì số (ValueError) Tại Chức năng 2, nếu nhập quantity là chữ cái (VD: hai, abc), dùng try...except bắt lỗi ValueError.

    Output: "Vui lòng nhập số lượng là một số nguyên!".
    Logging: Ghi log ERROR: ValueError - Invalid quantity input.
    sử dụng try-except với trường hợp là value error để bắt lỗi và gán kiểu dữ liệu cho biến nhập là int
Bẫy 2 — Lỗi mã đồ uống không tồn tại (ItemNotFoundError) Tạo một Custom Exception tên là ItemNotFoundError. Nếu drink_code nhập vào không có trong DRINK_MENU, raise lỗi này.

Bắt lỗi và Output: "Mã đồ uống không hợp lệ, vui lòng kiểm tra lại thực đơn!".
Logging: Ghi log WARNING: ItemNotFoundError - Code: [drink_code].
    sử dụng vòng lặp for kết hợp với điều kiện if-else để kiểm tra sự tồn tại của mã đồ uống được nhập vào 
Bẫy 3 — Lỗi số lượng âm hoặc bằng 0 (InvalidQuantityError) Tạo một Custom Exception tên là InvalidQuantityError. Nếu nhân viên nhập số lượng <= 0, raise lỗi này.

Bắt lỗi và Output: "Số lượng phải lớn hơn 0!".
Logging: Ghi log WARNING: InvalidQuantityError - Quantity: [quantity].
    sau khi try-except bắt những lỗi như nhập chữ hoặc nhập trống, dùng if-else để so sánh giá trị của biến nhập vào 
'''