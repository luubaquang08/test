import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://the-internet.herokuapp.com/login"

@pytest.fixture
def driver():
    """Khởi tạo trình duyệt Chrome trước mỗi bài test và tự động đóng sau khi xong."""
    options = webdriver.ChromeOptions()
    # Tắt cảnh báo và tối ưu hóa khi chạy kiểm thử tự động
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_success(driver):
    """
    Test Case 1: Đăng nhập thành công với tài khoản và mật khẩu hợp lệ.
    Kết quả mong đợi: Chuyển hướng tới trang /secure và hiển thị thông báo thành công.
    """
    # 1. Mở trang đăng nhập
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # 2. Định vị phần tử bằng By.ID và nhập thông tin hợp lệ
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password_field = driver.find_element(By.ID, "password")
    
    username_field.clear()
    username_field.send_keys("tomsmith")
    password_field.clear()
    password_field.send_keys("SuperSecretPassword!")

    # 3. Nhấn nút Đăng nhập
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # 4. Kiểm tra kết quả mong đợi
    # Kiểm tra URL đã chuyển sang trang bảo mật
    assert "/secure" in driver.current_url, "Lỗi: Không chuyển hướng đến trang /secure"

    # Kiểm tra thông báo hiển thị trên màn hình
    flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "You logged into a secure area!" in flash_message, "Lỗi: Không tìm thấy thông báo đăng nhập thành công"
    print("\n[TC01 - PASS] Đăng nhập thành công!")

def test_login_invalid_username(driver):
    """
    Test Case 2: Đăng nhập thất bại do nhập sai tên đăng nhập.
    Kết quả mong đợi: Vẫn ở trang /login và hiển thị thông báo lỗi 'Your username is invalid!'.
    """
    # 1. Mở trang đăng nhập
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # 2. Nhập username sai và password đúng
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password_field = driver.find_element(By.ID, "password")
    
    username_field.clear()
    username_field.send_keys("wrong_user")
    password_field.clear()
    password_field.send_keys("SuperSecretPassword!")

    # 3. Nhấn nút Đăng nhập
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # 4. Kiểm tra kết quả mong đợi
    flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "Your username is invalid!" in flash_message, "Lỗi: Thông báo sai tên đăng nhập không chính xác"
    print("\n[TC02 - PASS] Phát hiện đúng lỗi sai tên đăng nhập!")

def test_login_invalid_password(driver):
    """
    Test Case 3: Đăng nhập thất bại do nhập sai mật khẩu.
    Kết quả mong đợi: Vẫn ở trang /login và hiển thị thông báo lỗi 'Your password is invalid!'.
    """
    # 1. Mở trang đăng nhập
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # 2. Nhập username đúng và password sai
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password_field = driver.find_element(By.ID, "password")
    
    username_field.clear()
    username_field.send_keys("tomsmith")
    password_field.clear()
    password_field.send_keys("WrongPassword123")

    # 3. Nhấn nút Đăng nhập
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # 4. Kiểm tra kết quả mong đợi
    flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "Your password is invalid!" in flash_message, "Lỗi: Thông báo sai mật khẩu không chính xác"
    print("\n[TC03 - PASS] Phát hiện đúng lỗi sai mật khẩu!")