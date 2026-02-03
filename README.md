# Real-Time Logistics System 🚀

A production-ready, event-driven microservices system simulating a real-time logistics backend (inspired by Uber/Swiggy). This project demonstrates modern distributed systems architecture with event streaming, state management, and real-time notifications.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [Running with Kubernetes](#running-with-kubernetes)
- [API Documentation](#api-documentation)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

### Starting the System

```bash
# Start Kubernetes (if using)
minikube start

# Start Docker services
cd infrastructure
docker-compose up -d
```

### Stopping the System

```bash
# Stop Docker services
docker-compose down

# Stop Kubernetes (if using)
minikube stop
```

---

## 🏗 Architecture

```
┌─────────┐      ┌──────────────┐      ┌───────┐
│  Client │─────▶│  Order API   │─────▶│ Kafka │
└─────────┘      │  (FastAPI)   │      │       │
                 └──────────────┘      └───┬───┘
                        │                   │
                        │                   │ Events
                        ▼                   │
                   ┌────────┐              │
                   │ Redis  │◀─────────────┼────────┐
                   │ Cache  │              │        │
                   └────────┘              ▼        │
                                    ┌─────────────────────┐
                                    │ Order Processor     │
                                    │ (Consumer)          │
                                    └──────────┬──────────┘
                                               │
                                               │ Publishes
                                               ▼
                                    ┌─────────────────────┐
                                    │ Notification Service│
                                    │ (Consumer)          │
                                    └─────────────────────┘
```

### Event Flow

1. **Client** sends order creation request to **Order API**
2. **Order API** publishes "PLACED" event to Kafka topic
3. **Order Processor** consumes event, stores state in Redis
4. **Order Processor** simulates status transitions (CONFIRMED → PREPARING → OUT_FOR_DELIVERY → DELIVERED)
5. **Notification Service** consumes status change events and displays notifications

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Programming language |
| **FastAPI** | REST API framework |
| **Apache Kafka** | Event streaming platform |
| **Zookeeper** | Kafka coordination |
| **Redis** | In-memory state storage |
| **Docker & Docker Compose** | Containerization |
| **Kubernetes** | Container orchestration |
| **kafka-python** | Kafka client library |

---

## 📁 Project Structure

```
realtime-logistics-system/
├── infrastructure/
│   ├── docker-compose.yml          # Docker services configuration
│   └── k8s/                         # Kubernetes manifests
│       ├── order-api-deployment.yaml
│       ├── order-api-service.yaml
│       ├── order-processor.yaml
│       ├── redis-deployment.yaml
│       └── redis-service.yaml
├── services/
│   ├── order_api/                   # FastAPI REST API
│   │   ├── main.py                  # API endpoints
│   │   ├── producer.py              # Standalone producer script
│   │   ├── consumer.py              # Standalone consumer script
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── order_processor/             # Order state machine
│   │   ├── consumer.py              # Order processing logic
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── notification_service/        # Notification handler
│       ├── consumer.py              # Notification display logic
│       ├── Dockerfile
│       └── requirements.txt
├── venv/                            # Python virtual environment
├── requirements.txt                 # Project dependencies
└── README.md                        # This file
```

---

## ✨ Features

- ✅ **Event-Driven Architecture** - Loose coupling between services
- ✅ **Real-Time Order Tracking** - Live status updates
- ✅ **State Management** - Redis for persistent order state
- ✅ **Async Processing** - Non-blocking order lifecycle
- ✅ **Scalable Microservices** - Independent service deployment
- ✅ **Container-Ready** - Docker and Kubernetes support
- ✅ **Health Checks** - Service availability monitoring

---

## 📦 Prerequisites

### For Local Development
- Python 3.9 or higher
- Kafka (with Zookeeper)
- Redis
- pip

### For Docker
- Docker Desktop (or Docker Engine + Docker Compose)
- Minimum 4GB RAM allocated to Docker

### For Kubernetes
- Minikube or Docker Desktop with Kubernetes enabled
- kubectl CLI

---

## 💻 Running Locally

### Step 1: Clone and Setup Virtual Environment

```bash
# Navigate to project directory
cd realtime-logistics-system

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Infrastructure Services

**Option A: Using Homebrew (macOS)**

```bash
# Install and start Redis
brew install redis
brew services start redis

# Install and start Kafka
brew install kafka
brew services start zookeeper
brew services start kafka
```

**Option B: Using Docker for Infrastructure Only**

```bash
cd infrastructure
docker-compose up zookeeper kafka redis -d
```

### Step 3: Run the Services

**Terminal 1 - Order API:**
```bash
cd services/order_api
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Order Processor:**
```bash
cd services/order_processor
python consumer.py
```

**Terminal 3 - Notification Service:**
```bash
cd services/notification_service
python consumer.py
```

### Step 4: Test the System

```bash
# Create an order
curl -X POST http://localhost:8000/orders

# Response:
# {"message":"Order created","order_id":"abc12345"}

# Wait 10 seconds for processing, then check status
curl http://localhost:8000/orders/abc12345

# Response:
# {"order_id":"abc12345","status":"DELIVERED"}
```

---

## 🐳 Running with Docker

### Step 1: Navigate to Infrastructure Directory

```bash
cd infrastructure
```

### Step 2: Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

This will start:
- Zookeeper (Kafka coordination)
- Kafka broker (port 9092)
- Redis (port 6379)
- Order API (port 8000)
- Order Processor
- Notification Service

### Step 3: Verify Services are Running

```bash
docker-compose ps
```

You should see all services with status "Up" or "healthy":

```
NAME                                    STATUS
infrastructure-kafka-1                  Up (healthy)
infrastructure-notification_service-1   Up
infrastructure-order_api-1              Up
infrastructure-order_processor-1        Up
infrastructure-redis-1                  Up (healthy)
infrastructure-zookeeper-1              Up
```

### Step 4: Test the System

```bash
# Create an order
curl -X POST http://localhost:8000/orders

# Wait 10 seconds and check the logs
docker-compose logs order_processor
docker-compose logs notification_service
```

**Expected Output in Order Processor:**
```
Order Processor Running...
Received order abc12345 with status PLACED
Moved order abc12345 → CONFIRMED
Received order abc12345 with status CONFIRMED
Moved order abc12345 → PREPARING
...
Moved order abc12345 → DELIVERED
```

**Expected Output in Notification Service:**
```
Notification Service Running...
🔔 NOTIFICATION:
Order abc12345 is now CONFIRMED
🔔 NOTIFICATION:
Order abc12345 is now PREPARING
...
```

### Step 5: Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate - removes all data)
docker-compose down -v
```

**Quick Commands:**
- **Start:** `docker-compose up -d`
- **Stop:** `docker-compose down`
- **Restart:** `docker-compose restart`
- **View logs:** `docker-compose logs -f`

---

## ☸️ Running with Kubernetes

### Prerequisites

**Enable Kubernetes in Docker Desktop:**
1. Open Docker Desktop → Settings → Kubernetes
2. Check "Enable Kubernetes"
3. Click "Apply & Restart"

**Or install Minikube:**
```bash
brew install minikube
minikube start
```

### Step 1: Build Docker Images

```bash
# Build all service images
cd services/order_api
docker build -t order_api:latest .

cd ../order_processor
docker build -t order_processor:latest .

cd ../notification_service
docker build -t notification_service:latest .
```

### Step 2: Deploy Infrastructure (Redis)

```bash
cd infrastructure/k8s

# Deploy Redis
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
```

### Step 3: Deploy Kafka (Manual Setup Required)

Kafka requires special setup in Kubernetes. Use a Helm chart:

```bash
# Add Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install Kafka
helm install kafka bitnami/kafka \
  --set replicaCount=1 \
  --set zookeeper.enabled=true \
  --set deleteTopicEnable=true
```

Wait for Kafka to be ready:
```bash
kubectl get pods -w
```

### Step 4: Deploy Application Services

```bash
# Deploy Order API
kubectl apply -f order-api-deployment.yaml
kubectl apply -f order-api-service.yaml

# Deploy Order Processor
kubectl apply -f order-processor.yaml
```

### Step 5: Verify Deployments

```bash
# Check all pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -f deployment/order-api
kubectl logs -f deployment/order-processor
```

### Step 6: Access the API

```bash
# Get the service URL
# For Docker Desktop Kubernetes:
kubectl get service order-api

# Access the API at:
# http://localhost:30007
```

### Step 7: Test the System

```bash
# Create an order
curl -X POST http://localhost:30007/orders

# Check order status
curl http://localhost:30007/orders/{order_id}
```

### Step 8: Scale Services

```bash
# Scale order processor to 3 replicas
kubectl scale deployment order-processor --replicas=3

# Verify scaling
kubectl get pods
```

### Step 9: Clean Up

```bash
# Delete all resources
kubectl delete -f order-api-deployment.yaml
kubectl delete -f order-api-service.yaml
kubectl delete -f order-processor.yaml
kubectl delete -f redis-deployment.yaml
kubectl delete -f redis-service.yaml

# Uninstall Kafka
helm uninstall kafka
```

**Quick Commands:**
- **Start Minikube:** `minikube start`
- **Stop Minikube:** `minikube stop`
- **Delete Minikube:** `minikube delete` (removes all data)
- **View status:** `kubectl get pods`
- **View logs:** `kubectl logs -f deployment/order-api`

---

## 📡 API Documentation

### Base URL
- **Local:** `http://localhost:8000`
- **Docker:** `http://localhost:8000`
- **Kubernetes:** `http://localhost:30007`

### Endpoints

#### 1. Create Order

**Request:**
```http
POST /orders
```

**Response:**
```json
{
  "message": "Order created",
  "order_id": "abc12345"
}
```

**Status Code:** `200 OK`

---

#### 2. Get Order Status

**Request:**
```http
GET /orders/{order_id}
```

**Response (Success):**
```json
{
  "order_id": "abc12345",
  "status": "DELIVERED"
}
```

**Response (Not Found):**
```json
{
  "error": "Order not found"
}
```

**Status Codes:**
- `200 OK` - Order found
- `404 Not Found` - Order doesn't exist

---

## 🔄 How It Works

### Order Status Flow

```
PLACED → CONFIRMED → PREPARING → OUT_FOR_DELIVERY → DELIVERED
```

Each transition takes approximately **2 seconds** to simulate real processing time.

### Component Responsibilities

#### 1. **Order API Service** (`order_api/main.py`)
- **POST /orders**: Creates new order
  - Generates unique order ID
  - Publishes "PLACED" event to Kafka `orders` topic
  - Returns order ID to client
- **GET /orders/{id}**: Retrieves order status
  - Queries Redis for current status
  - Returns status or 404 error

#### 2. **Order Processor** (`order_processor/consumer.py`)
- Consumes events from `orders` topic
- Maintains order state machine
- Stores current status in Redis (`order:{id}`)
- Publishes next status event to `orders` topic
- Publishes notification event to `order_notifications` topic
- Processes status transitions every 2 seconds

#### 3. **Notification Service** (`notification_service/consumer.py`)
- Consumes events from `order_notifications` topic
- Displays user-friendly notifications
- Simulates push notifications or email alerts

---

## 🐛 Troubleshooting

### Issue: Kafka "NoBrokersAvailable" Error

**Symptoms:**
```
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
```

**Solutions:**

1. **Docker:** Ensure Kafka health check passes
   ```bash
   docker-compose ps
   # Wait until kafka shows "healthy"
   ```

2. **Local:** Check Kafka is running
   ```bash
   # macOS
   brew services list | grep kafka
   
   # Or check the process
   ps aux | grep kafka
   ```

3. **Network:** Verify connection
   ```bash
   nc -zv localhost 9092
   ```

---

### Issue: Redis Connection Refused

**Symptoms:**
```
redis.exceptions.ConnectionError: Error 111 connecting to redis:6379
```

**Solutions:**

1. **Check Redis is running:**
   ```bash
   # Docker
   docker-compose ps redis
   
   # Local
   redis-cli ping
   # Should return: PONG
   ```

2. **Check Redis host configuration:**
   - Local: Use `localhost`
   - Docker: Use `redis` (service name)
   - Kubernetes: Use `redis` (service name)

---

### Issue: Port Already in Use

**Symptoms:**
```
Error: bind: address already in use
```

**Solutions:**

1. **Find process using port:**
   ```bash
   # macOS/Linux
   lsof -i :8000
   lsof -i :9092
   lsof -i :6379
   ```

2. **Kill the process:**
   ```bash
   kill -9 <PID>
   ```

3. **Or stop conflicting Docker services:**
   ```bash
   docker-compose down
   ```

---

### Issue: Docker Images Not Found in Kubernetes

**Symptoms:**
```
Failed to pull image "order_api:latest": ImagePullBackOff
```

**Solutions:**

1. **For Docker Desktop Kubernetes:**
   ```bash
   # Build images directly
   cd services/order_api
   docker build -t order_api:latest .
   ```

2. **For Minikube:**
   ```bash
   # Use Minikube's Docker daemon
   eval $(minikube docker-env)
   
   # Then build images
   docker build -t order_api:latest .
   ```

3. **Verify image exists:**
   ```bash
   docker images | grep order_api
   ```

---

### Issue: Services Start Before Kafka is Ready

**Symptoms:**
- Services crash and restart multiple times
- "Connection refused" errors in logs

**Solution:**

This is handled by health checks in `docker-compose.yml`:

```yaml
depends_on:
  kafka:
    condition: service_healthy
```

If services still fail, increase health check intervals or add manual delay.

---

### Viewing Logs

**Docker:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f order_processor

# Last 50 lines
docker-compose logs --tail=50 order_api
```

**Kubernetes:**
```bash
# View pod logs
kubectl logs -f pod/order-api-xxxxx

# View deployment logs
kubectl logs -f deployment/order-processor

# Stream logs
kubectl logs -f -l app=order-api
```

---

## 📊 Monitoring

### Check Kafka Topics

```bash
# Docker
docker exec -it infrastructure-kafka-1 kafka-topics --list --bootstrap-server localhost:9092

# Expected topics:
# - orders
# - order_notifications
```

### Check Redis Keys

```bash
# Docker
docker exec -it infrastructure-redis-1 redis-cli

# In Redis CLI:
127.0.0.1:6379> KEYS *
127.0.0.1:6379> GET order:abc12345
```

---

## 🚀 Future Enhancements

- [ ] Add authentication & authorization
- [ ] Implement GraphQL API
- [ ] Add Prometheus metrics
- [ ] Add distributed tracing (Jaeger/Zipkin)
- [ ] Implement dead letter queues
- [ ] Add event replay capability
- [ ] Create admin dashboard
- [ ] Add integration tests
- [ ] Implement circuit breakers
- [ ] Add API rate limiting

---

## 📝 License

This is a learning project. Feel free to use and modify as needed.

---

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome!

---

## 📧 Contact

For questions or discussions about this project, please open an issue.

---

## 🎓 Learning Resources

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ as a microservices learning project**
