import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restaurant Ordering System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
BG_COLOR = (156, 147, 115)
MENU_BG_COLOR = (115, 129, 156)
THANK_BG_COLOR = (235, 167, 232)

clock = pygame.time.Clock()
# Fonts
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40, bold=True)

# Classes
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
        item.quantity += 1
        if item not in self.items:
            self.items.append(item)

    def remove_item(self, item):
        if item.quantity > 0:
            item.quantity -= 1
        if item.quantity == 0 and item in self.items:
            self.items.remove(item)

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items)

class FoodOrderingApp:
    def __init__(self):
        # Original menu (for buttons)
        self.menu = [
            FoodItem("Burger", 5.99, pygame.Rect(50, 120, 250, 60)),
            FoodItem("Pizza", 8.99, pygame.Rect(50, 200, 250, 60)),
            FoodItem("Salad", 4.99, pygame.Rect(50, 280, 250, 60)),
            FoodItem("Drink", 1.99, pygame.Rect(50, 360, 250, 60)),
        ]

        # Start with a fresh order
        self.current_order = self.create_new_order()
        self.place_order_button = pygame.Rect(400, 500, 200, 60)
        self.back_button = pygame.Rect(650, 500, 200, 60)
        self.running = True
        self.order_placed = False

    # Create a new order with fresh FoodItem objects
    def create_new_order(self):
        order = Order()
        for menu_item in self.menu:
            new_item = FoodItem(menu_item.name, menu_item.price, menu_item.rect)
            order.items.append(new_item)  # start with 0 quantity
        return order

    def draw_button(self, rect, text, color=GRAY, hover_color=THANK_BG_COLOR):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, rect, border_radius=20)
        else:
            pygame.draw.rect(screen, color, rect, border_radius=10)
        label = font.render(text, True, BLACK)
        text_rect = label.get_rect(center=rect.center)
        screen.blit(label, text_rect)

    def display_menu(self):
        for i, menu_item in enumerate(self.menu):
            pygame.draw.rect(screen, GRAY, menu_item.rect, border_radius=10)
            label = font.render(f"{menu_item.name} - ${menu_item.price:.2f}", True, BLACK)
            screen.blit(label, (menu_item.rect.x + 10, menu_item.rect.y + 15))

            # Plus and minus buttons
            plus_btn = pygame.Rect(menu_item.rect.x + 250 + 10, menu_item.rect.y, 40, 60)
            minus_btn = pygame.Rect(menu_item.rect.x + 250 + 60, menu_item.rect.y, 40, 60)
            self.draw_button(plus_btn, "+", BLUE)
            self.draw_button(minus_btn, "-", RED)

            menu_item.plus_btn = plus_btn
            menu_item.minus_btn = minus_btn

    def display_order(self):
        pygame.draw.rect(screen, LIGHT_GRAY, pygame.Rect(405, 100, 550, 380), border_radius=10)
        title = title_font.render("Current Order", True, GREEN)
        screen.blit(title, (420, 110))

        y = 160
        any_items = False
        for menu_item in self.menu:
            # Find corresponding item in current_order
            order_item = next((item for item in self.current_order.items if item.name == menu_item.name), None)
            if order_item and order_item.quantity > 0:
                label = font.render(f"{order_item.name} x{order_item.quantity} - ${order_item.price * order_item.quantity:.2f}", True, BLACK)
                screen.blit(label, (420, y))
                y += 30
                any_items = True

        if not any_items:
            label = font.render("No items yet.", True, BLACK)
            screen.blit(label, (420, y))

        total_label = font.render(f"Total: ${sum(item.price * item.quantity for item in self.current_order.items if item.quantity > 0):.2f}", True, RED)
        screen.blit(total_label, (420, y + 40))

    def thank_you_screen(self):
        screen.fill(BG_COLOR)
        msg = title_font.render("Thank you for ordering", True, THANK_BG_COLOR)
        msg2 = title_font.render("Sorry for being late TnT", True, WHITE)

        try:
            sori = pygame.image.load('sori.png')
            sori = pygame.transform.scale(sori, (int(sori.get_width() * 0.5), int(sori.get_height() * 0.5)))
            srect = sori.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
            screen.blit(sori, srect)
        except:
            pass

        screen.blit(msg2, (270, 20))
        screen.blit(msg, (WIDTH // 2 - 220, HEIGHT // 2 + 120))
        self.draw_button(self.back_button, "Back to Menu", BG_COLOR)
        pygame.display.flip()

    def run(self):
        
        while self.running:
            screen.fill(MENU_BG_COLOR)
            header = title_font.render("Restaurant Ordering System", True, BLACK)
            screen.blit(header, (WIDTH // 2 - 250, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.order_placed:
                        # Check plus/minus buttons
                        for i, menu_item in enumerate(self.menu):
                            order_item = next((item for item in self.current_order.items if item.name == menu_item.name), None)
                            if order_item:
                                if menu_item.plus_btn.collidepoint(pos):
                                    order_item.quantity += 1
                                elif menu_item.minus_btn.collidepoint(pos):
                                    if order_item.quantity > 0:
                                        order_item.quantity -= 1

                        if self.place_order_button.collidepoint(pos):
                            self.order_placed = True
                    else:
                        if self.back_button.collidepoint(pos):
                            # Create a completely fresh order
                            self.current_order = self.create_new_order()
                            self.order_placed = False

            if self.order_placed:
                self.thank_you_screen()
            else:
                self.display_menu()
                self.display_order()
                self.draw_button(self.place_order_button, "Place Order", RED)

            pygame.display.update()

        pygame.quit()
        sys.exit()


# Run the app
app = FoodOrderingApp()
app.run()
