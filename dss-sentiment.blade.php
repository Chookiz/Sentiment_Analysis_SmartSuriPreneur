<div class="row mt-0 mt-lg-12">

    <div class="col-xl-10 form-container">
        <div class="card shadow-sm d-flex flex-column" style="height: auto;">
            <div class="card-body d-flex flex-column p-3 ">
                <h2>Tambah Komen Baharu</h2>
                <form id="insertReviewForm">
                    <div class="form-group">
                        <label for="name">Nama *</label>
                        <input type="text" class="form-control" id="name" name="name" placeholder="Masukkan nama produk" required>
                    </div>
                    <div class="form-group">
                        <label for="comment">Komen *</label>
                        <textarea class="form-control" id="comment" name="comment" rows="3" placeholder="Masukkan review/komen mengenai produk" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="sold">Jualan</label>
                        <input type="number" class="form-control" id="sold" name="sold" placeholder="Masukkan jumlah jualan (tidak wajib)" min="0">
                    </div>
                    <div class="form-group">
                        <label for="price">Harga</label>
                        <input type="number" class="form-control" id="price" name="price" placeholder="Masukkan harga (tidak wajib)" min="0" step="0.01">
                    </div>
                    <div class="form-group">
                        <label for="stock">Stok</label>
                        <input type="number" class="form-control" id="stock" name="stock" placeholder="Masukkan stok (tidak wajib)" min="0">
                    </div>
                    <input type="hidden" id="sentiment" name="sentiment">
                    <input type="hidden" id="kategori" name="kategori">
                    <button type="submit" class="btn btn-primary">Hantar</button>
                </form>
            </div>
        </div>
    

    
        <div class="card shadow-sm mt-4 d-flex flex-column" style="height: auto;">
            <div class="card-body d-flex flex-column justify-content-center align-items-center p-3 text-center">
                <div>
                    <img class="m-auto" width="80%" src="{{ asset('assets/media/placeholder/analissentimen.png') }}">
                </div>
                <div class="w-100 mt-3 d-flex justify-content-center">
                    <div class="form-floating mb-2 w-50">
                        <input type="text" class="form-control" wire:model.lazy="namaProduk" placeholder="Carian"/>
                        <label class="form-select-sm" for="floatingInput">Carian</label>
                    </div>
                    <a wire:click="submit" class="btn btn-sm btn-primary ms-2 align-self-start">Papar</a>
                </div>
            </div>
        </div>

        <div class="card shadow-sm mt-4 d-flex flex-column" style="height: auto;">
            <div class="card-body p-3 text-center">
                <div id="chart-container" style="position: relative; width: 100%; height: 75vh;">
                    <canvas id="chart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

@push('page-script')
<style>
    #chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 75vh; /* Adjust this as needed */
    }
    #chart {
        width: 100%;
        height: 100% !important;
    }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('livewire:load', function () {
        const ctx = document.getElementById('chart').getContext('2d');
        let chart;

        Livewire.on('updateChart', data => {
            console.log('Data received:', data);

            const labels = Object.values(data.labels);
            const datasets = data.datasets.map(dataset => ({
                ...dataset,
                data: Object.values(dataset.data)
            }));

            console.log('Transformed data:', { labels, datasets });

            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: datasets
                },
                options: {
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    elements: {
                        bar: {
                            borderWidth: 1,
                        }
                    },
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        },
                        title: {
                            display: true,
                            text: 'Graf Sentimen'
                        }
                    }
                }
            });

            // Adjust card height to fit the chart
            adjustCardHeight();
        });

        function adjustCardHeight() {
            const chartContainer = document.getElementById('chart-container');
            const card = chartContainer.closest('.card');
            if (chart) {
                card.style.height = chart.height + 'px';
            }
        }
    });
</script>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('insertReviewForm').addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const data = {
                name: formData.get('name'),
                comment: formData.get('comment'),
                sold: formData.get('sold') || 0,
                price: formData.get('price') || 0,
                stock: formData.get('stock') || 0,
            };

            fetch('http://127.0.0.1:8000/sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                alert('Review berjaya dihantar.');
                document.getElementById('insertReviewForm').reset(); // Reset form fields
                } else {
                    alert('Error: ' + (result.error || 'An unknown error occurred'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting the review.');
            });
        });
    });
</script>
@endpush
