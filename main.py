import keyboard
import time

count = 0

print("=== 스페이스바 카운터 시작 ===")
print("스페이스바(Space)를 누르면 카운터가 1씩 올라갑니다.")
print("종료하려면 'Esc' 키를 누르세요.\n")

def on_space(event):
    global count
    count += 1
    print(f"현재 카운트: {count}")

# 스페이스바 키를 누를 때 on_space 함수 실행
keyboard.on_press_key("space", on_space)

# 프로그램이 바로 종료되지 않도록 'esc' 누를 때까지 대기
keyboard.wait("esc")
print("\n프로그램을 종료합니다.")
