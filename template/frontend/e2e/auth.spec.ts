/**
 * Authentication E2E tests.
 */

import { expect, test } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Clear local storage before each test
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('shows login page', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByPlaceholder('メールアドレス')).toBeVisible();
    await expect(page.getByPlaceholder('パスワード')).toBeVisible();
    await expect(page.getByRole('button', { name: 'ログイン' })).toBeVisible();
  });

  test('shows test account info', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByText('テストアカウント:')).toBeVisible();
    await expect(page.getByText('Email: test@example.com')).toBeVisible();
  });

  test('can type in login form', async ({ page }) => {
    await page.goto('/');

    await page.getByPlaceholder('メールアドレス').fill('test@example.com');
    await page.getByPlaceholder('パスワード').fill('password');

    await expect(page.getByPlaceholder('メールアドレス')).toHaveValue(
      'test@example.com'
    );
    await expect(page.getByPlaceholder('パスワード')).toHaveValue('password');
  });

  test('shows error on invalid credentials', async ({ page }) => {
    await page.goto('/');

    await page.getByPlaceholder('メールアドレス').fill('wrong@example.com');
    await page.getByPlaceholder('パスワード').fill('wrongpassword');
    await page.getByRole('button', { name: 'ログイン' }).click();

    // Wait for error message
    await expect(page.getByText(/ログインに失敗|Invalid/)).toBeVisible({
      timeout: 10000,
    });
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await page.goto('/');

    await page.getByPlaceholder('メールアドレス').fill('test@example.com');
    await page.getByPlaceholder('パスワード').fill('password');
    await page.getByRole('button', { name: 'ログイン' }).click();

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });

    // Should show welcome message
    await expect(page.getByText(/ようこそ/)).toBeVisible();
  });

  test('dashboard shows user info', async ({ page }) => {
    // Login first
    await page.goto('/');
    await page.getByPlaceholder('メールアドレス').fill('test@example.com');
    await page.getByPlaceholder('パスワード').fill('password');
    await page.getByRole('button', { name: 'ログイン' }).click();

    // Wait for dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });

    // Should show user info
    await expect(page.getByText('ユーザー情報')).toBeVisible();
    await expect(page.getByText('test@example.com')).toBeVisible();
  });

  test('logout redirects to login page', async ({ page }) => {
    // Login first
    await page.goto('/');
    await page.getByPlaceholder('メールアドレス').fill('test@example.com');
    await page.getByPlaceholder('パスワード').fill('password');
    await page.getByRole('button', { name: 'ログイン' }).click();

    // Wait for dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });

    // Click logout
    await page.getByRole('button', { name: 'ログアウト' }).click();

    // Should redirect to login
    await expect(page).toHaveURL('/', { timeout: 10000 });
  });
});
