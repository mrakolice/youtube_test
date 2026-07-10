FROM node:18-alpine

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml* ./

RUN pnpm install

RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "dev", "--host", "0.0.0.0"]
