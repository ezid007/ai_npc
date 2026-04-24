#!/usr/bin/env python3
"""pgvector 연결 테스트 스크립트"""

import psycopg


# 환경 변수 로드
def load_env():
    env = {}
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


env = load_env()

# PostgreSQL 연결 설정
conn_params = {
    "host": env.get("POSTGRES_HOST", "localhost"),
    "port": int(env.get("POSTGRES_PORT", "5432")),
    "dbname": env.get("POSTGRES_DB", "ai_npc_db"),
    "user": env.get("POSTGRES_USER", "postgres"),
    "password": env.get("POSTGRES_PASSWORD", ""),
}

print("PostgreSQL 연결 테스트")
print("=" * 50)

try:
    with psycopg.connect(**conn_params) as conn:
        print("✅ PostgreSQL 연결 성공!")
        print(f"PostgreSQL 버전: {conn.info.server_version}")

        with conn.cursor() as cur:
            # pgvector 확인
            cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
            result = cur.fetchone()
            if result:
                print(f"✅ pgvector 설치됨 (버전: {result[5]})")
            else:
                print("❌ pgvector 가 설치되지 않았습니다.")

            # 테스트
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS test_vectors (
                    id SERIAL PRIMARY KEY,
                    embedding vector(3)
                )
            """
            )
            conn.commit()

            cur.execute(
                "INSERT INTO test_vectors (embedding) VALUES (%s)", ("[1,2,3]",)
            )
            conn.commit()

            cur.execute("SELECT embedding FROM test_vectors ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            if row:
                print(f"✅ 벡터 테스트 성공: {row[0]}")

            # 정리
            cur.execute("DROP TABLE IF EXISTS test_vectors;")
            conn.commit()
            print("✅ 테스트 완료!")

except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback

    traceback.print_exc()
