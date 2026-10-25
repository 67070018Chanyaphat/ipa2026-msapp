import os, time, pika
from callback import callback  # Import ฟังก์ชัน callback มาจากไฟล์ callback.py[cite: 7]

# ดึงค่า Username และ Password จาก Environment Variables[cite: 3, 7]
user = os.getenv("RABBITMQ_DEFAULT_USER")
pwd = os.getenv("RABBITMQ_DEFAULT_PASS")


def consume(host):
    # วนลูปพยายามเชื่อมต่อ RabbitMQ สูงสุด 10 ครั้ง กรณีที่ RabbitMQ Server ยังเปิดไม่เสร็จ[cite: 3, 7]
    for attempt in range(10):
        try:
            print(f"Connecting to RabbitMQ (try {attempt})...")
            creds = pika.PlainCredentials(user, pwd)
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(host, credentials=creds)
            )
            break
        except Exception as e:
            print(f"Failed: {e}")
            time.sleep(5)
    else:
        print("Could not connect after 10 attempts")
        exit(1)

    ch = conn.channel()
    ch.queue_declare(
        queue="router_jobs"
    )  # ประกาศชื่อ Queue ที่ต้องการรับงาน[cite: 4, 7]
    ch.basic_qos(prefetch_count=1)  # ดึงงานมาทำทีละ 1 Message เท่านั้น[cite: 4, 7]

    # กำหนดให้เมื่อมี Message เข้ามา ให้เรียกใช้ฟังก์ชัน callback ที่ import มา[cite: 4, 7]
    ch.basic_consume(queue="router_jobs", on_message_callback=callback, auto_ack=True)
    ch.start_consuming()


if __name__ == "__main__":
    consume("localhost")
