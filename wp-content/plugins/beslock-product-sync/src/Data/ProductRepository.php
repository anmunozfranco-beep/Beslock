<?php

declare(strict_types=1);

namespace Beslock\ProductSync\Data;

final class ProductRepository
{
    public function __construct(private string $productsJsonPath)
    {
    }

    /**
     * @return array<int, array<string, mixed>>
     */
    public function all(): array
    {
        if (! is_readable($this->productsJsonPath)) {
            return [];
        }

        $raw = file_get_contents($this->productsJsonPath);
        if ($raw === false) {
            return [];
        }

        $decoded = json_decode($raw, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            error_log(sprintf('Beslock product sync: invalid JSON in %s (%s)', $this->productsJsonPath, json_last_error_msg()));
            return [];
        }

        return is_array($decoded) ? $decoded : [];
    }
}
