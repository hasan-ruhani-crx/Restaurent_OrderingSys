import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restaurant Ordering System")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
RANDOM = (156, 147, 115)
RANDOM2 = (115, 129, 156)
RANDOM3=(235, 167, 232)


font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40, bold=True)

class FoodItem:
    def __init__(self, name, price, rect):
        self.name = name
        self.price = price
        self.rect = rect
        self.quantity = 0


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
        item.quantity += 1

    def remove_item(self, item):
        if item.quantity > 0:
            item.quantity -= 1
        if item.quantity == 0 and item in self.items:
            self.items.remove(item)

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items)

class FoodOrderingApp:
    def __init__(self):
        self.menu = [
            FoodItem("Burger", 5.99, pygame.Rect(50, 120, 250, 60)),
            FoodItem("Pizza", 8.99, pygame.Rect(50, 200, 250, 60)),
            FoodItem("Salad", 4.99, pygame.Rect(50, 280, 250, 60)),
            FoodItem("Drink", 1.99, pygame.Rect(50, 360, 250, 60)),
        ]
        self.current_order = Order()
        self.place_order_button = pygame.Rect(400, 500, 200, 60)
        self.back_button = pygame.Rect(650, 500, 200, 60)
        self.running = True
        self.order_placed = False

    def draw_button(self, rect, text, color=GRAY,hover_color = RANDOM3):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, rect, border_radius=20)
        else:
            pygame.draw.rect(screen, color, rect, border_radius=10)
        label = font.render(text, True, BLACK)
        screen.blit(label, (rect.x + 10, rect.y + rect.height//2 - 12))

    def display_menu(self):
        for item in self.menu:
            pygame.draw.rect(screen, GRAY, item.rect, border_radius=10)
            label = font.render(f"{item.name} - ${item.price:.2f}", False, BLACK)
            screen.blit(label, (item.rect.x + 10, item.rect.y + 15))

            # Add + and - buttons
            plus_btn = pygame.Rect(item.rect.x + 250+10, item.rect.y, 40, 60)
            minus_btn = pygame.Rect(item.rect.x + 250+60, item.rect.y, 40, 60)
            self.draw_button(plus_btn, "+", BLUE)
            self.draw_button(minus_btn, "-", RED)

            item.plus_btn = plus_btn
            item.minus_btn = minus_btn

    def display_order(self):
        pygame.draw.rect(screen, LIGHT_GRAY , pygame.Rect(405, 100, 550, 380), border_radius= 10)
        title = title_font.render("Current Order", True, GREEN)
        screen.blit(title, (420, 110))

        y = 160
        for item in self.current_order.items:
            label = font.render(f"{item.name} x{item.quantity} - ${item.price*item.quantity:.2f}", True, BLACK)
            screen.blit(label, (420, y))
            y += 30

        total_label = font.render(f"Total: ${self.current_order.total_price():.2f}", True, RED)
        screen.blit(total_label, (420, y + 20))

    def thank_you_screen(self):
        screen.fill(RANDOM)
        msg = title_font.render("Thank you for ordering", True, RANDOM3)
        msg2 = title_font.render("Sorry for being late TnT" , True , WHITE )
        sori = pygame.image.load('sori.png')
        sori = pygame.transform.scale(sori, (sori.get_width()*.5, sori.get_height()*.5))
        screen.blit(msg2,(270,20))
        srect = sori.get_rect(center=(WIDTH//2, HEIGHT//2-60))
        screen.blit(sori,srect)
        screen.blit(msg, (WIDTH//2 - 220, HEIGHT//2 + 120))
        self.draw_button(self.back_button, "Back to Menu", RANDOM)
        pygame.display.flip()

    def run(self):
        while self.running:
            screen.fill(RANDOM2)
            header = title_font.render("Restaurant Ordering System", True, BLACK)
            screen.blit(header, (WIDTH//2 - 250, 30))

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # print("Mouse clicked :", pos)
                    if not self.order_placed:
                        for item in self.menu:
                            if item.plus_btn.collidepoint(pos):
                                self.current_order.add_item(item)
                            elif item.minus_btn.collidepoint(pos):
                                self.current_order.remove_item(item)
                        if self.place_order_button.collidepoint(pos):
                            self.order_placed = True
                    else:
                        if self.back_button.collidepoint(pos):
                            self.order_placed = False
                            for item in self.menu:
                                item.quantity = 0
                            self.current_order = Order() 
            if self.order_placed:
                self.thank_you_screen()
            else:
                self.display_menu()
                self.display_order()
                self.draw_button(self.place_order_button, "Place Order", RED)

            pygame.display.update()

        pygame.quit()
        sys.exit()


app = FoodOrderingApp()
app.run()
