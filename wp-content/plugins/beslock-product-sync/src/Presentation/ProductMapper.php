<?php

declare(strict_types=1);

namespace Beslock\ProductSync\Presentation;

final class ProductMapper
{
    /**
     * @param array<string, mixed> $raw
     * @return array{title:string,slug:string,description:string,price:string}
     */
    public function map(array $raw): array
    {
        $price = trim((string) ($raw['price'] ?? ''));
        $isValidPrice = $price !== '' && is_numeric($price) && (float) $price >= 0;

        return [
            'title' => (string) ($raw['title'] ?? ''),
            'slug' => sanitize_title((string) ($raw['slug'] ?? $raw['title'] ?? '')),
            'description' => (string) ($raw['description'] ?? ''),
            'price' => $isValidPrice ? $price : '',
        ];
    }
}
