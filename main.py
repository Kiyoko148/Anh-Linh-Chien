import pygame
import sys
from pygame.locals import *
import time
import random

pygame.init()
pygame.mixer.init()

# Cài đặt cửa sổ
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Tên game
pygame.display.set_caption(r'Anh Linh Chiến')

# Biểu tượng game
icon = pygame.image.load(r'Background\icon.jpg')
pygame.display.set_icon(icon)

# Background
main_screen = pygame.image.load(r'Background\main_screen.jpg')

# Nhạc nền
pygame.mixer.music.load(r"Nhạc nền.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# Cài đặt màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CORAL = (255,127,80)

# Hàm vẽ văn bản
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

# Hàm vẽ văn bản căn giữa
def draw_text_centered(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Hàm vẽ nút "Chơi Ngay"
show_play_button = True  
def draw_play_button():
    if show_play_button:
        button_rect = pygame.Rect(430, 550, 150, 50)
        pygame.draw.rect(screen, CORAL, button_rect, border_radius = 10)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius = 10)  # Vẽ viền cho nút
        button_text = draw_text_centered("Chơi Ngay", font, WHITE, screen, button_rect.centerx, button_rect.centery)
        return button_rect  # Trả về hình dạng của nút để kiểm tra khi click
    else:
        # Không vẽ nút nếu show_play_button là False
        return None

# Hàm kiểm tra va chạm chuột với nút "Chơi Ngay"
def check_button_click():
    if show_play_button:
        button_rect = pygame.Rect(430, 550, 150, 50)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            return True
    return False
    
# Chỉ số cơ bản của Anh Linh
class AnhLinh:
    def __init__(self, ten, he_chien_dau, loai_al, bac_al, image_path):
        self.ten = ten
        self.chi_mang = 0.3
        self.he_chien_dau = he_chien_dau
        self.loai_al = loai_al
        self.bac_al = bac_al
        self._initialize_stats(None, None)
        self.loai_anh_linh()
        self.image = pygame.image.load(image_path)
        self.xuat_chien = 0
    
    def _initialize_stats(self, trangbi_HK ,trangbi_TV):
        # Khởi tạo chỉ số dựa trên bậc Anh Linh
        stats = {
        "R": {"tan_cong": 80, "phong_thu": 20, "tri_lieu": 50, "hp": 500},
        "SR": {"tan_cong": 120, "phong_thu": 30, "tri_lieu": 60, "hp": 550},
        "SSR": {"tan_cong": 160, "phong_thu": 40, "tri_lieu": 70, "hp": 600},
        }
        base_stats = stats.get(self.bac_al)
        if base_stats:
            for stat, value in base_stats.items():
                setattr(self, stat, value)
        
        # Trang bị Hồn Khí được thêm chỉ số
        if trangbi_HK == True:
            self.tan_cong += 50
            self.phong_thu += 50
            self.hp += 100
            
        # Trang bị Thần Võ được thêm chỉ số
        if trangbi_TV == True:    
            self.tan_cong += 50
            self.phong_thu += 50
            self.hp += 100
        
        self.loai_anh_linh()
        
    # Ràng buộc điều kiện chỉ số cho Anh Linh
    def loai_anh_linh(self):

        #Với Anh Linh loại tấn công và phòng thủ sẽ không có chỉ số trị liệu
        if self.loai_al == "Tấn Công":
            self.tri_lieu = 0
        elif self.loai_al == "Phòng Thủ":
            self.tri_lieu = 0

        #Với Anh Linh loại tấn công và trị liệu chỉ có một nửa phòng thủ
        if self.loai_al == "Tấn Công":
            self.phong_thu /= 2
        elif self.loai_al == "Trị Liệu":
            self.phong_thu /= 2

        #Với Anh Linh loại phòng thủ và trị liệu sẽ bị giảm một nửa tấn công
        if self.loai_al == "Phòng Thủ":
            self.tan_cong /= 2
        elif self.loai_al == "Trị Liệu":
            self.tan_cong /= 2

        # Với Anh Linh phòng thủ được tăng phòng thủ
        if self.loai_al == "Phòng Thủ":
            self.phong_thu *= 2

        # Với Anh Linh trị liệu được tăng hp
        elif self.loai_al == "Trị Liệu":
            self.hp *= 2

    #Hàm tấn công
    def tinh_sat_thuong(self, KeDich):
        sat_thuong = self.tan_cong - KeDich.phong_thu / 2
        if sat_thuong <= 0:
            sat_thuong = 50
        if random.random() < self.chi_mang:
            sat_thuong *= 2
        if self.he_chien_dau == "Hỏa" and KeDich.he_chien_dau == "Lôi":
            sat_thuong *= 1.5
        elif self.he_chien_dau == "Lôi" and KeDich.he_chien_dau == "Thủy":
            sat_thuong *= 1.5
        elif self.he_chien_dau == "Thủy" and KeDich.he_chien_dau == "Hỏa":
            sat_thuong *= 1.5
        elif self.he_chien_dau == "Quang" and KeDich.he_chien_dau == "Ám":
            sat_thuong *= 1.5
        elif self.he_chien_dau == "Ám" and KeDich.he_chien_dau == "Quang":
            sat_thuong *= 1.5
        return sat_thuong


class KeDich(AnhLinh):
    def __init__(self, ten, he_chien_dau, loai_al, bac_al, image_path):
        super().__init__(ten, he_chien_dau, loai_al, bac_al, image_path)

    def _enemy_initialize_stats(KeDich):
        # Khởi tạo chỉ số dựa trên bậc Anh Linh
        stats = {
        "R": {"tan_cong": 250, "phong_thu": 50, "tri_lieu": 100, "hp": 800},
        "SR": {"tan_cong": 300, "phong_thu": 80, "tri_lieu": 120, "hp": 1000}
        }
        base_stats = stats.get(KeDich.bac_al)
        if base_stats:
            for stat, value in base_stats.items():
                setattr(KeDich, stat, value)
        
        KeDich.loai_anh_linh()
        
# Khởi tạo các Anh Linh

# Anh Linh R
AnhLinh_R = [
    AnhLinh("Lôi Khắc", "Lôi", "Tấn Công", "R", r'Anh Linh\R\Lôi Khắc.png'),
    AnhLinh("Thổ Dã", "Quang", "Phòng Thủ", "R", r'Anh Linh\R\Thổ Dã.png'),
    AnhLinh("Tiểu Tân", "Thủy", "Trị Liệu", "R", r'Anh Linh\R\Tiểu Tân.png')
]

# Anh Linh SR
AnhLinh_SR = [
    AnhLinh("Anh Sơn", "Ám", "Phòng Thủ", "SR", r'Anh Linh\SR\Anh Sơn.png'),
    AnhLinh("Sương Quả", "Thủy", "Trị Liệu", "SR", r'Anh Linh\SR\Sương Quả.png'),
    AnhLinh("Thương Diên", "Hỏa", "Tấn Công", "SR", r'Anh Linh\SR\Thương Diên.png')
]

# Anh Linh SSR
AnhLinh_SSR = [
    AnhLinh("Aniya", "Quang", "Trị Liệu", "SSR", r'Anh Linh\SSR\Aniya.png'),
    AnhLinh("Hoang Liệt", "Hỏa", "Tấn Công", "SSR", r'Anh Linh\SSR\Hoang Liệt.png'),
    AnhLinh("Tiêu", "Lôi", "Phòng Thủ", "SSR", r'Anh Linh\SSR\Tiêu.png')
]

# Hàm vẽ khung thông tin của anh linh xuất chiến
def draw_info_frame():
    info_rect = pygame.Rect(80, 375, 320, 270)
    pygame.draw.rect(screen, WHITE, info_rect, border_radius = 10)
    pygame.draw.rect(screen, BLACK, info_rect, 2, border_radius = 10)
    draw_text("THÔNG TIN CƠ BẢN", font, 'BLACK', screen, 120, 375)
    draw_text("- Tên:", font, 'BLACK', screen, 100, 400)
    draw_text("- Hệ:", font, 'BLACK', screen, 100, 430)
    draw_text("- Dạng:", font, 'BLACK', screen, 100, 460)
    draw_text("- Bậc:", font, 'BLACK', screen, 100, 490)
    draw_text("- Tấn Công:", font, 'BLACK', screen, 100, 520)
    draw_text("- Phòng Thủ:", font, 'BLACK', screen, 100, 550)
    draw_text("- Trị Liệu:", font, 'BLACK', screen, 100, 580)
    draw_text("- HP:", font, 'BLACK', screen, 100, 610)
    
# Khung thông tin của kẻ địch
def draw_enemy_info_frame():
    enemy_info_rect = pygame.Rect(620, 65, 320, 270)
    pygame.draw.rect(screen, WHITE, enemy_info_rect, border_radius = 10)
    pygame.draw.rect(screen, BLACK, enemy_info_rect, 2, border_radius = 10)
    draw_text("THÔNG TIN CƠ BẢN", font, 'BLACK', screen, 660, 70)
    draw_text("- Tên:", font, 'BLACK', screen, 640, 90)
    draw_text("- Hệ:", font, 'BLACK', screen, 640, 120)
    draw_text("- Dạng:", font, 'BLACK', screen, 640, 150)
    draw_text("- Bậc:", font, 'BLACK', screen, 640, 180)
    draw_text("- Tấn Công:", font, 'BLACK', screen, 640, 210)
    draw_text("- Phòng Thủ:", font, 'BLACK', screen, 640, 240)
    draw_text("- Trị Liệu:", font, 'BLACK', screen, 640, 270)
    draw_text("- HP:", font, 'BLACK', screen, 640, 300)
  
def main():
    # Load font
    global font
    font = pygame.font.SysFont('Times New Roman', 24)
    
    # Thiết lập trạng thái
    running = True
    prepare = False
    fighting = False
    start = False
    
    # Trạng thái chiến đấu
    win = False
    lose = False
    
    # Thiết lập khung chọn anh linh
    khung_chon = pygame.Rect(70, 610, 60, 85)
    MAX_x = 870
    MIN_x = 70
    temp = 100
            
    #Vòng lặp chính
    while running:
        screen.blit(main_screen, (0, 0))
        draw_play_button()
        
        for event in pygame.event.get():
            
            #Thoát game
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            # Bắt đầu game sau khi click chơi ngay
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_click():
                    show_play_button = False
                    prepare = True
            
            # Dùng nút di chuyển trái phải để chọn Anh Linh xuất chiến
            elif event.type == pygame.KEYDOWN:
                if prepare:
                    
                    # Thay đổi vị trí khung để người chơi lựa chọn
                    if event.key == pygame.K_RIGHT:
                        pygame.draw.rect(screen, 'gray', khung_chon)
                        if khung_chon.x < MAX_x:
                            khung_chon.x += temp
                    elif event.key == pygame.K_LEFT:
                        pygame.draw.rect(screen, 'gray', khung_chon)
                        if khung_chon.x > MIN_x:
                            khung_chon.x -= temp

                    # Nhấn phím SPACE để chọn Anh Linh
                    elif event.key == pygame.K_SPACE:
                        
                        # Chọn Lôi Khắc
                        if khung_chon.x == 70:
                            LoiKhac.xuat_chien = 1
                            
                        # Chọn Thổ Dã
                        elif khung_chon.x == 170:
                            ThoDa.xuat_chien = 1
                        
                        # Chọn Tiểu Tân
                        elif khung_chon.x == 270:
                            TieuTan.xuat_chien = 1
                        
                        # Chọn Anh Sơn 
                        elif khung_chon.x == 370:
                            AnhSon.xuat_chien = 1
                            
                        # Chọn Sương Quả
                        elif khung_chon.x == 470:
                            SuongQua.xuat_chien = 1
                            
                        # Chọn Thương Diên
                        elif khung_chon.x == 570:
                            ThuongDien.xuat_chien = 1
                        
                        # Chọn Aniya
                        elif khung_chon.x == 670:
                            Aniya.xuat_chien = 1
                        
                        # Chọn Hoang Liệt    
                        elif khung_chon.x == 770:
                            HoangLiet.xuat_chien = 1
                        
                        # Chọn Tiêu    
                        elif khung_chon.x == 870:
                            Tieu.xuat_chien = 1
                            
                        khung_chon.x = 470
                        khung_chon.y = 395
                        temp = 0
                    
                    # Nhấn phím BACKSPACE để lựa chọn lại
                    elif event.key == pygame.K_BACKSPACE:
                        khung_chon.y = 610
                        temp = 100
                        if LoiKhac.xuat_chien == 1:
                            LoiKhac.xuat_chien = 0
                            khung_chon.x = 70
                        
                        elif ThoDa.xuat_chien == 1:
                            ThoDa.xuat_chien = 0
                            khung_chon.x = 170
                        
                        elif TieuTan.xuat_chien == 1:
                            TieuTan.xuat_chien = 0
                            khung_chon.x = 270
                            
                        elif AnhSon.xuat_chien == 1:
                            AnhSon.xuat_chien = 0
                            khung_chon.x = 370
                            
                        elif SuongQua.xuat_chien == 1:
                            SuongQua.xuat_chien = 0
                            khung_chon.x = 470
                            
                        elif ThuongDien.xuat_chien == 1:
                            ThuongDien.xuat_chien = 0
                            khung_chon.x = 570
                            
                        elif Aniya.xuat_chien == 1:
                            Aniya.xuat_chien = 0
                            khung_chon.x = 670
                            
                        elif HoangLiet.xuat_chien == 1:
                            HoangLiet.xuat_chien = 0
                            khung_chon.x = 770
                            
                        elif Tieu.xuat_chien == 1:
                            Tieu.xuat_chien = 0
                            khung_chon.x = 870
                    
                    # Nhấn ENTER để xác nhận chọn Anh Linh        
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if LoiKhac.xuat_chien == 1 or ThoDa.xuat_chien == 1 or TieuTan.xuat_chien == 1 or AnhSon.xuat_chien == 1 or SuongQua.xuat_chien == 1 or ThuongDien.xuat_chien == 1 or Aniya.xuat_chien == 1 or HoangLiet.xuat_chien == 1 or Tieu.xuat_chien == 1:
                            prepare = False
                            fighting = True
                            start = True
                
                # Thoát về màn hình chính nếu ấn nút ESCAPE
                if event.key == pygame.K_ESCAPE:
                    show_play_button = True
                    prepare = False
                    fighting = False
                    screen.blit(main_screen, (0, 0))
                    draw_play_button()
                       
        # Chuẩn bị/Giao diện chọn Anh Linh
        if prepare:
            screen.fill('gray')
            bg1 = pygame.image.load(r'Background\sàn đấu.png')
            screen.blit(bg1, (0, 0))
            rect0 = pygame.Rect(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 110, 300, 50)
            pygame.draw.rect(screen, CORAL, rect0, border_radius = 10)
            draw_text("Chọn Anh Linh xuất chiến", font, WHITE, screen, SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 100)
            
            # Tạo khung hiển thị Anh Linh đang chọn
            pygame.draw.rect(screen, GREEN, khung_chon)
            
            #Danh sách lựa chọn Anh Linh
            
            # Bậc R
            LoiKhac = AnhLinh_R[0]
            screen.blit(LoiKhac.image, (75, 615))
            ThoDa = AnhLinh_R[1]
            screen.blit(ThoDa.image, (175, 615))
            TieuTan = AnhLinh_R[2]
            screen.blit(TieuTan.image, (275, 615))
            
            # Bậc SR
            AnhSon = AnhLinh_SR[0]
            screen.blit(AnhSon.image, (375, 615))
            SuongQua = AnhLinh_SR[1]
            screen.blit(SuongQua.image, (475, 615))
            ThuongDien = AnhLinh_SR[2]
            screen.blit(ThuongDien.image, (575, 615))
            
            # Bậc SSR
            Aniya = AnhLinh_SSR[0]
            screen.blit(Aniya.image, (675, 615))
            HoangLiet = AnhLinh_SSR[1]
            screen.blit(HoangLiet.image, (775, 615))
            Tieu = AnhLinh_SSR[2]
            screen.blit(Tieu.image, (875, 615))
            
            # Khi chọn Lôi Khắc xuất chiến
            if LoiKhac.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (75, 615, 50, 75))
                screen.blit(LoiKhac.image, (475, 400))
                
            # Khi chọn Thổ Dã xuất chiến
            elif ThoDa.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (175, 615, 50, 75))
                screen.blit(ThoDa.image, (475, 400))
                
            # Khi chọn Tiểu Tân xuất chiến
            elif TieuTan.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (275, 615, 50, 75))
                screen.blit(TieuTan.image, (475, 400))
                
            # Khi chọn Anh Sơn xuất chiến
            elif AnhSon.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (375, 615, 50, 75))
                screen.blit(AnhSon.image, (475, 400))
                
            # Khi chọn Sương Quả xuất chiến
            elif SuongQua.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (475, 615, 50, 75))
                screen.blit(SuongQua.image, (475, 400))
                
            # Khi chọn Thương Diên xuất chiến
            elif ThuongDien.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (575, 615, 50, 75))
                screen.blit(ThuongDien.image, (475, 400))
            
            # Khi chọn Aniya xuất chiến    
            elif Aniya.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (675, 615, 50, 75))
                screen.blit(Aniya.image, (475, 400))
            
            # Khi chọn Hoang Liệt xuất chiến
            elif HoangLiet.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (775, 615, 50, 75))
                screen.blit(HoangLiet.image, (475, 400))
            
            # Khi chọn Tiêu xuất chiến
            elif Tieu.xuat_chien == 1:
                pygame.draw.rect(screen, 'gray', (875, 615, 50, 75))
                screen.blit(Tieu.image, (475, 400))
                
            pygame.display.flip()
    
        random_index = random.randint(0, 5)
        # Môi trường chiến đấu
        if fighting:
            screen.fill(BLACK)
            screen.blit(bg1, (0, 50))
            
            # In chữ "Chuẩn bị chiến đấu" và bước vào chiến đấu sau 5s
            if start:
                draw_text("Chuẩn bị chiến đấu", font, WHITE, screen, SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 100)
                pygame.display.flip()
                time.sleep(5)
                screen.fill(BLACK)
                screen.blit(bg1, (0, 50))
                start = False
                  
            draw_info_frame()
            draw_enemy_info_frame()
            
            HonKhi = pygame.image.load(r'Hồn Khí.png')
            screen.blit(HonKhi, (750, 390))
            ThanVo = pygame.image.load(r'Thần Võ.png')
            screen.blit(ThanVo, (750, 520))
            
            # Thông tin cụ thể
            # Khi chọn Lôi Khắc xuất chiến
            if LoiKhac.xuat_chien == 1:
                loikhac = pygame.image.load(r'Anh Linh\R\Lôi Khắc (1).png')
                screen.blit(loikhac, (450, 450))
                LoiKhac._initialize_stats(True, True)
                draw_text("Lôi Khắc", font, 'BLACK', screen, 250, 400)
                draw_text("Lôi", font, 'purple', screen, 250, 430)
                draw_text("Tấn Công", font, 'darkred', screen, 250, 460)
                draw_text("R", font, 'darkblue', screen, 250, 490)
                draw_text(f"{LoiKhac.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{LoiKhac.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{LoiKhac.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{LoiKhac.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = LoiKhac
                 
            # Khi chọn Thổ Dã xuất chiến
            elif ThoDa.xuat_chien == 1:
                thoda = pygame.image.load(r'Anh Linh\R\Thổ Dã (1).png')
                screen.blit(thoda, (450, 450))
                ThoDa._initialize_stats(True, True)
                draw_text("Thổ Dã", font, BLACK, screen, 250, 400)
                draw_text("Quang", font, 'brown', screen, 250, 430)
                draw_text("Phòng Thủ", font, 'orange', screen, 250, 460)
                draw_text("R", font, 'darkblue', screen, 250, 490)
                draw_text(f"{ThoDa.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{ThoDa.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{ThoDa.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{ThoDa.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = ThoDa
                
            # Khi chọn Tiểu Tân xuất chiến
            elif TieuTan.xuat_chien == 1:
                tieutan = pygame.image.load(r'Anh Linh\R\Tiểu Tân (1).png')
                screen.blit(tieutan, (450, 450))
                TieuTan._initialize_stats(True, True)
                draw_text("Tiểu Tân", font, BLACK, screen, 250, 400)
                draw_text("Thủy", font, 'blue', screen, 250, 430)
                draw_text("Trị Liệu", font, 'green', screen, 250, 460)
                draw_text("R", font, 'darkblue', screen, 250, 490)
                draw_text(f"{TieuTan.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{TieuTan.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{TieuTan.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{TieuTan.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = TieuTan
                
            # Khi chọn Anh Sơn xuất chiến
            elif AnhSon.xuat_chien == 1:
                anhson = pygame.image.load(r'Anh Linh\SR\Anh Sơn (1).png')
                screen.blit(anhson, (450, 450))
                AnhSon._initialize_stats(True, True)
                draw_text("Anh Sơn", font, BLACK, screen, 250, 400)
                draw_text("Ám", font, 'black', screen, 250, 430)
                draw_text("Phòng Thủ", font, 'brown', screen, 250, 460)
                draw_text("SR", font, 'orchid', screen, 250, 490)
                draw_text(f"{AnhSon.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{AnhSon.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{AnhSon.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{AnhSon.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = AnhSon
                
            # Khi chọn Sương Quả xuất chiến
            elif SuongQua.xuat_chien == 1:
                suongqua = pygame.image.load(r'Anh Linh\SR\Sương Quả (1).png')
                screen.blit(suongqua, (450, 450))
                SuongQua._initialize_stats(True, True)
                draw_text("Sương Quả", font, BLACK, screen, 250, 400)
                draw_text("Thủy", font, 'blue', screen, 250, 430)
                draw_text("Trị Liệu", font, 'green', screen, 250, 460)
                draw_text("SR", font, 'orchid', screen, 250, 490)
                draw_text(f"{SuongQua.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{SuongQua.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{SuongQua.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{SuongQua.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = SuongQua
                
            # Khi chọn Thương Diên xuất chiến
            elif ThuongDien.xuat_chien == 1:
                thuongdien = pygame.image.load(r'Anh Linh\SR\Thương Diên (1).png')
                screen.blit(thuongdien, (450, 450))
                ThuongDien._initialize_stats(True, True)
                draw_text("Thương Diên", font, BLACK, screen, 250, 400)
                draw_text("Hỏa", font, 'red', screen, 250, 430)
                draw_text("Tấn Công", font, 'darkred', screen, 250, 460)
                draw_text("SR", font, 'orchid', screen, 250, 490)
                draw_text(f"{ThuongDien.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{ThuongDien.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{ThuongDien.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{ThuongDien.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = ThuongDien
            
            # Khi chọn Aniya xuất chiến    
            elif Aniya.xuat_chien == 1:
                aniya = pygame.image.load(r'Anh Linh\SSR\Aniya (1).png')
                screen.blit(aniya, (450, 450))
                Aniya._initialize_stats(True, True)
                draw_text("Aniya", font, BLACK, screen, 250, 400)
                draw_text("Quang", font, 'brown', screen, 250, 430)
                draw_text("Trị Liệu", font, 'green', screen, 250, 460)
                draw_text("SSR", font, (255, 215, 0), screen, 250, 490)
                draw_text(f"{Aniya.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{Aniya.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{Aniya.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{Aniya.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = Aniya
            
            # Khi chọn Hoang Liệt xuất chiến
            elif HoangLiet.xuat_chien == 1:
                hoangliet = pygame.image.load(r'Anh Linh\SSR\Hoang Liệt (1).png')
                screen.blit(hoangliet, (450, 450))
                HoangLiet._initialize_stats(True, True)
                draw_text("Hoang Liệt", font, BLACK, screen, 250, 400)
                draw_text("Hỏa", font, 'red', screen, 250, 430)
                draw_text("Tấn Công", font, 'darkred', screen, 250, 460)
                draw_text("SSR", font, (255, 215, 0), screen, 250, 490)
                draw_text(f"{HoangLiet.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{HoangLiet.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{HoangLiet.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{HoangLiet.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = HoangLiet
            
            # Khi chọn Tiêu xuất chiến
            elif Tieu.xuat_chien == 1:
                tieu = pygame.image.load(r'Anh Linh\SSR\Tiêu (1).png')
                screen.blit(tieu, (450, 450))
                Tieu._initialize_stats(True, True)
                draw_text("Tiêu", font, BLACK, screen, 250, 400)
                draw_text("Lôi", font, 'purple', screen, 250, 430)
                draw_text("Phòng Thủ", font, 'brown', screen, 250, 460)
                draw_text("SSR", font, (255, 215, 0), screen, 250, 490)
                draw_text(f"{Tieu.tan_cong}", font, 'BLACK', screen, 250, 520)
                draw_text(f"{Tieu.phong_thu}", font, 'BLACK', screen, 250, 550)
                draw_text(f"{Tieu.tri_lieu}", font, 'BLACK', screen, 250, 580)
                draw_text(f"{Tieu.hp}", font, 'BLACK', screen, 250, 610)
                anhlinh = Tieu
            
            # Khi Lôi Khắc làm kẻ địch
            if random_index == 0:
                Loi_Khac = KeDich("Lôi Khắc", "Lôi", "Tấn Công", "R", r'Anh Linh\R\Lôi Khắc.png')
                Loi_Khac._enemy_initialize_stats()
                loikhac = pygame.image.load(r'Anh Linh\R\Lôi Khắc (1).png')
                screen.blit(loikhac, (450, 150))
                draw_text("Lôi Khắc", font, 'BLACK', screen, 800, 90)
                draw_text("Lôi", font, 'purple', screen, 800, 120)
                draw_text("Tấn Công", font, 'darkred', screen, 800, 150)
                draw_text("R", font, 'darkblue', screen, 800, 180)
                draw_text(f"{Loi_Khac.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Loi_Khac.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Loi_Khac.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Loi_Khac.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Loi_Khac
                                
            # Khi Thổ Dã làm kẻ địch
            elif random_index == 1:
                Tho_Da = KeDich("Thổ Dã", "Quang", "Phòng Thủ", "R", r'Anh Linh\R\Thổ Dã.png')
                Tho_Da._enemy_initialize_stats()
                thoda = pygame.image.load(r'Anh Linh\R\Thổ Dã (1).png')
                screen.blit(thoda, (450, 150))
                draw_text("Thổ Dã", font, BLACK, screen, 800, 90)
                draw_text("Quang", font, 'brown', screen, 800, 120)
                draw_text("Phòng Thủ", font, 'orange', screen, 800, 150)
                draw_text("R", font, 'darkblue', screen, 800, 180)
                draw_text(f"{Tho_Da.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Tho_Da.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Tho_Da.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Tho_Da.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Tho_Da
                            
            # Khi Tiểu Tân làm kẻ địch
            elif random_index == 2:
                Tieu_Tan = KeDich("Tiểu Tân", "Thủy", "Trị Liệu", "R", r'Anh Linh\R\Tiểu Tân.png')
                Tieu_Tan._enemy_initialize_stats()
                tieutan = pygame.image.load(r'Anh Linh\R\Tiểu Tân (1).png')
                screen.blit(tieutan, (450, 150))
                draw_text("Tiểu Tân", font, BLACK, screen, 800, 90)
                draw_text("Thủy", font, 'blue', screen, 800, 120)
                draw_text("Trị Liệu", font, 'green', screen, 800, 150)
                draw_text("R", font, 'darkblue', screen, 800, 180)
                draw_text(f"{Tieu_Tan.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Tieu_Tan.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Tieu_Tan.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Tieu_Tan.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Tieu_Tan
                
            # Khi Anh Sơn làm kẻ địch
            elif random_index == 3:
                Anh_Son = KeDich("Anh Sơn", "Ám", "Phòng Thủ", "SR", r'Anh Linh\SR\Anh Sơn.png')
                Anh_Son._enemy_initialize_stats()
                anhson = pygame.image.load(r'Anh Linh\SR\Anh Sơn (1).png')
                screen.blit(anhson, (450, 150))
                draw_text("Anh Sơn", font, BLACK, screen, 800, 90)
                draw_text("Ám", font, 'black', screen, 800, 120)
                draw_text("Phòng Thủ", font, 'brown', screen, 800, 150)
                draw_text("SR", font, 'orchid', screen, 800, 180)
                draw_text(f"{Anh_Son.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Anh_Son.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Anh_Son.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Anh_Son.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Anh_Son
                
            # Khi Sương Quả làm kẻ địch
            elif random_index == 4:
                Suong_Qua = KeDich("Sương Quả", "Thủy", "Trị Liệu", "SR", r'Anh Linh\SR\Sương Quả.png')
                Suong_Qua._enemy_initialize_stats()
                suongqua = pygame.image.load(r'Anh Linh\SR\Sương Quả (1).png')
                screen.blit(suongqua, (450, 150))
                draw_text("Sương Quả", font, BLACK, screen, 800, 90)
                draw_text("Thủy", font, 'blue', screen, 800, 120)
                draw_text("Trị Liệu", font, 'green', screen, 800, 150)
                draw_text("SR", font, 'orchid', screen, 800, 180)
                draw_text(f"{Suong_Qua.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Suong_Qua.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Suong_Qua.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Suong_Qua.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Suong_Qua
                
            # Khi Thương Diên làm kẻ địch
            elif random_index == 5:
                Thuong_Dien = KeDich("Thương Diên", "Hỏa", "Tấn Công", "SR", r'Anh Linh\SR\Thương Diên.png')
                Thuong_Dien._enemy_initialize_stats()
                thuongdien = pygame.image.load(r'Anh Linh\SR\Thương Diên (1).png')
                screen.blit(thuongdien, (450, 150))
                draw_text("Thương Diên", font, BLACK, screen, 800, 90)
                draw_text("Hỏa", font, 'red', screen, 800, 120)
                draw_text("Tấn Công", font, 'darkred', screen, 800, 150)
                draw_text("SR", font, 'orchid', screen, 800, 180)
                draw_text(f"{Thuong_Dien.tan_cong}", font, 'BLACK', screen, 800, 210)
                draw_text(f"{Thuong_Dien.phong_thu}", font, 'BLACK', screen, 800, 240)
                draw_text(f"{Thuong_Dien.tri_lieu}", font, 'BLACK', screen, 800, 270)
                draw_text(f"{Thuong_Dien.hp}", font, 'BLACK', screen, 800, 300)
                kedich = Thuong_Dien
            
            hp_AL_hientai = anhlinh.hp
            hp_KD_hientai = kedich.hp
            
            al_hoi_phuc = anhlinh.tri_lieu
            kd_hoi_phuc = kedich.tri_lieu
            
            # Kiểm tra Anh Linh có trị liệu chí mạng hay không
            if random.random() < anhlinh.chi_mang:
                al_hoi_phuc *= 2

            while not win and not lose:
                # Anh Linh tấn công
                sathuong_AL = anhlinh.tinh_sat_thuong(kedich)
                hp_KD_hientai -= sathuong_AL
                if hp_KD_hientai < 0:
                    hp_KD_hientai = 0
                if anhlinh.tri_lieu != 0:
                    hp_AL_hientai += al_hoi_phuc
                rect1 = pygame.Rect(800, 300, 100, 25)
                pygame.draw.rect(screen, WHITE, rect1)
                draw_text(f"{hp_KD_hientai}", font, 'BLACK', screen, 800, 300)
                
                # Kiểm tra nếu Anh Linh bị hạ gục
                if hp_AL_hientai <= 0:
                    lose = True
                    break
                
                # Kẻ địch tấn công
                sathuong_KD = kedich.tinh_sat_thuong(anhlinh)
                hp_AL_hientai -= sathuong_KD
                if hp_AL_hientai < 0:
                    hp_AL_hientai = 0
                if kedich.tri_lieu != 0:
                    hp_KD_hientai += kd_hoi_phuc
                rect2 = pygame.Rect(250, 610, 100, 25)
                pygame.draw.rect(screen, WHITE, rect2)
                draw_text(f"{hp_AL_hientai}", font, 'BLACK', screen, 250, 610)
                
                # Kiểm tra nếu Anh Linh hạ gục kẻ địch
                if hp_KD_hientai <= 0:
                    win = True
                    break
                pygame.display.flip() 
            
            # Về màn hình chính nếu bị thất bại
            if lose:
                rect3 = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 10, 150, 50)
                pygame.draw.rect(screen, WHITE, rect3, border_radius = 10)
                draw_text("THUA CUỘC", font, BLACK, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                time.sleep(5)
                # Reset lại trò chơi
                show_play_button = True
                fighting = False
                screen.blit(main_screen, (0, 0))
                draw_play_button()
                lose = False
                
                
            # Trở về màn hình chính nếu thắng lợi    
            elif win:
                rect3 = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 10, 150, 50)
                pygame.draw.rect(screen, WHITE, rect3, border_radius = 10)
                draw_text("THẮNG LỢI", font, BLACK, screen, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                time.sleep(5)
                # Reset lại trò chơi
                show_play_button = True
                fighting = False
                screen.blit(main_screen, (0, 0))
                draw_play_button()
                win = False
                
        pygame.display.update()        
        pygame.time.Clock().tick(60)  # Điều chỉnh tốc độ hiển thị
        
if __name__ == "__main__":
    main()