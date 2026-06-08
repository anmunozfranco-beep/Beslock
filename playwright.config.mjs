import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.PW_BASE_URL || 'http://localhost:8080';

export default defineConfig({
  testDir: './tests/playwright',
  outputDir: './test-results/playwright',
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  use: {
    baseURL,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  webServer: process.env.PW_SKIP_WEBSERVER
    ? undefined
    : {
        command: 'docker compose up -d',
        url: baseURL,
        reuseExistingServer: true,
        timeout: 60000,
      },
  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1600, height: 900 },
      },
    },
    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 5'],
      },
    },
  ],
});
