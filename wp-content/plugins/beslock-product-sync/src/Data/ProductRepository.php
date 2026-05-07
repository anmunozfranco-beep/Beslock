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

        $decoded = json_decode((string) file_get_contents($this->productsJsonPath), true);

        return is_array($decoded) ? $decoded : [];
    }
}
