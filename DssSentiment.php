<?php

namespace App\Http\Livewire;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

use Livewire\Component;


class DssSentiment extends Component
{ 
    public $namaProduk;
    public $labels = [], $dataset = [];
    
    public function submit() {
        
    $this -> labels = [];
    $this -> dataset = [];

    if (empty($this->namaProduk)) {
        return redirect()->back()->with('error', 'Isi nama dahulu');
    }
    else{
        $this->loadData();
    }    
    
    }
    
    public function loadData()
    {
        if (empty($this->namaProduk)) {
            return;
        }

        $response = Http::get("http://127.0.0.1:8000/sentiment/{$this->namaProduk}");
        $data = $response->json();

        $positiveData = array_filter($data, fn($item) => $item['sentiment'] === 1);
        $negativeData = array_filter($data, fn($item) => $item['sentiment'] === 0);

        $productNames = array_unique(array_merge(
            array_map(fn($item) => $item['name'], $positiveData),
            array_map(fn($item) => $item['name'], $negativeData)
        ));

        $this->labels = array_values(array_map('strval', $productNames));

        $positiveCounts = array_map(function($name) use ($positiveData) {
            return count(array_filter($positiveData, fn($item) => $item['name'] === $name));
        }, $this->labels);

        $negativeCounts = array_map(function($name) use ($negativeData) {
            return count(array_filter($negativeData, fn($item) => $item['name'] === $name));
        }, $this->labels);

        $this->dataset = [
            [
                'label' => 'Positive',
                'backgroundColor'=> 'rgba(0, 128, 0, 0.7)', 
                'borderColor'=> 'rgba(0, 128, 0, 1)', 
                'borderWidth' => 1,
                'data' => array_values($positiveCounts),
            ],
            [
                'label' => 'Negative',
                'backgroundColor' => 'rgba(255, 0, 0, 0.7)',
                'borderColor' => 'rgba(255, 0, 0, 1)',
                'borderWidth' => 1,
                'data' => array_values($negativeCounts),
            ],
        ];

        // Debugging
        logger()->info('Labels:', $this->labels);
        logger()->info('Dataset:', $this->dataset);

        $this->emit('updateChart', [ 
            'labels'   => $this->labels,
            'datasets' => $this->dataset,
        ]);
    }


    public function updatedFilterName()
    {
        $this->loadData();
    }
}