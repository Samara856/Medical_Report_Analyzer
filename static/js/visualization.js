// static/js/visualization.js
class MedAnalyzerCharts {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        // Initialize file upload functionality
        this.initFileUpload();
        
        // Check if results data is available
        if (typeof resultData !== 'undefined' && resultData !== null) {
            this.createCharts();
            this.updateHealthAssessment();
        }
    }

    initFileUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const browseBtn = document.getElementById('browseBtn');
        
        // Check if elements exist
        if (!uploadArea || !fileInput || !browseBtn) return;
        
        // Click on upload area to trigger file input
        uploadArea.addEventListener('click', (e) => {
            // Only trigger file input if clicking on the upload area itself, not on the button
            if (e.target === uploadArea || e.target.classList.contains('upload-text') || 
                e.target.classList.contains('upload-subtext') || e.target.classList.contains('upload-icon')) {
                fileInput.click();
            }
        });
        
        // Click on browse button
        browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileInput.click();
        });
        
        // File selection
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                const uploadArea = document.getElementById('uploadArea');
                uploadArea.innerHTML = `<div class="upload-icon">✅</div>
                                        <p class="upload-text">${fileName}</p>
                                        <p class="upload-subtext" style="color: #06d6a0;">Ready to analyze</p>
                                        <button type="button" class="btn" id="browseBtn">Choose File</button>`;
                
                // Reattach event listener to the new button
                const newBrowseBtn = document.getElementById('browseBtn');
                if (newBrowseBtn) {
                    newBrowseBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        document.getElementById('fileInput').click();
                    });
                }
            }
        });
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.style.borderColor = '#4361ee';
                uploadArea.style.background = 'rgba(27, 69, 255, 0.1)';
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.style.borderColor = '#e9ecef';
                uploadArea.style.background = '#f8f9fa';
            }, false);
        });
        
        uploadArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            
            if (files.length > 0) {
                const fileName = files[0].name;
                const uploadArea = document.getElementById('uploadArea');
                uploadArea.innerHTML = `<div class="upload-icon">✅</div>
                                        <p class="upload-text">${fileName}</p>
                                        <p class="upload-subtext" style="color: #06d6a0;">Ready to analyze</p>
                                        <button type="button" class="btn" id="browseBtn">Choose File</button>`;
                
                // Reattach event listener to the new button
                const newBrowseBtn = document.getElementById('browseBtn');
                if (newBrowseBtn) {
                    newBrowseBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        document.getElementById('fileInput').click();
                    });
                }
            }
        });
    }

    createCharts() {
        // Extract data from the resultData object
        const { values, labels } = resultData;
        
        // Convert data for Chart.js
        const testData = Object.entries(values).map(([test, value]) => ({
            test: this.formatTestName(test),
            value: parseFloat(value),
            status: labels[test]
        }));

        // Create bar chart
        this.createBarChart(testData);
        
        // Create radar chart
        this.createRadarChart(testData);
        
        // Create doughnut chart for status distribution
        this.createStatusChart(labels);
    }

    formatTestName(testName) {
        return testName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    createBarChart(testData) {
        const ctx = document.getElementById('resultsChart');
        if (!ctx) return;

        const labels = testData.map(item => item.test);
        const data = testData.map(item => item.value);
        const backgroundColors = testData.map(item => this.getStatusColor(item.status, 0.8));
        const borderColors = testData.map(item => this.getStatusColor(item.status, 1));

        // Destroy existing chart if it exists
        if (this.charts.bar) {
            this.charts.bar.destroy();
        }

        this.charts.bar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Lab Results',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Value'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            color: '#495057'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Test'
                        },
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#495057',
                            autoSkip: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1,
                        cornerRadius: 6,
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const status = testData[context.dataIndex].status;
                                return `Value: ${context.parsed.y}, Status: ${status}`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    createRadarChart(testData) {
        const ctx = document.getElementById('radarChart');
        if (!ctx) return;

        // Normalize values for radar chart (scale to 0-100)
        const maxValue = Math.max(...testData.map(item => item.value));
        const normalizedData = testData.map(item => (item.value / maxValue) * 100);

        const backgroundColor = 'rgba(67, 97, 238, 0.2)';
        const borderColor = 'rgba(67, 97, 238, 1)';
        const pointBackgroundColors = testData.map(item => this.getStatusColor(item.status, 1));

        // Destroy existing chart if it exists
        if (this.charts.radar) {
            this.charts.radar.destroy();
        }

        this.charts.radar = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: testData.map(item => item.test),
                datasets: [{
                    label: 'Your Results (Normalized)',
                    data: normalizedData,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    pointBackgroundColor: pointBackgroundColors,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: borderColor
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            display: true,
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        pointLabels: {
                            color: '#495057'
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const originalValue = testData[context.dataIndex].value;
                                const status = testData[context.dataIndex].status;
                                return `Value: ${originalValue}, Status: ${status}`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    createStatusChart(labels) {
        const ctx = document.getElementById('statusChart');
        if (!ctx) return;

        // Count statuses
        const statusCounts = {
            Normal: 0,
            High: 0,
            Low: 0
        };

        Object.values(labels).forEach(status => {
            if (statusCounts.hasOwnProperty(status)) {
                statusCounts[status]++;
            }
        });

        const data = [statusCounts.Normal, statusCounts.High, statusCounts.Low];
        const backgroundColors = [
            this.getStatusColor('Normal', 0.8),
            this.getStatusColor('High', 0.8),
            this.getStatusColor('Low', 0.8)
        ];
        const borderColors = [
            this.getStatusColor('Normal', 1),
            this.getStatusColor('High', 1),
            this.getStatusColor('Low', 1)
        ];

        // Destroy existing chart if it exists
        if (this.charts.doughnut) {
            this.charts.doughnut.destroy();
        }

        this.charts.doughnut = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'High', 'Low'],
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} test(s) (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    getStatusColor(status, opacity) {
        const colors = {
                 Normal: "#3ba121ff",  // Bright green
                 High:   "#bb0a0aff",  // Vivid amber/orange
                 Low:    "#fae31aff"   // Strong red
                       };

        return colors[status] || `rgba(108, 117, 125, ${opacity})`;
    }

    updateHealthAssessment() {
        const { values, labels } = resultData;
        
        // Update status counts
        const normalCount = Object.values(labels).filter(status => status === 'Normal').length;
        const highCount = Object.values(labels).filter(status => status === 'High').length;
        const lowCount = Object.values(labels).filter(status => status === 'Low').length;
        const totalCount = Object.keys(labels).length;
        
        // Update counters
        const normalCountEl = document.getElementById('normalCount');
        const highCountEl = document.getElementById('highCount');
        const lowCountEl = document.getElementById('lowCount');
        
        if (normalCountEl) normalCountEl.textContent = normalCount;
        if (highCountEl) highCountEl.textContent = highCount;
        if (lowCountEl) lowCountEl.textContent = lowCount;

        // Calculate health score
        const healthScore = Math.round((normalCount / totalCount) * 100);
        
        // Animate health score
        this.animateHealthScore(healthScore);
        
        // Update score color based on value
        this.updateScoreColor(healthScore);
    }

    animateHealthScore(targetScore) {
        const scoreElement = document.getElementById('healthScore');
        const scoreDisplay = scoreElement ? scoreElement.querySelector('.score-text') : null;
        
        if (!scoreDisplay) return;
        
        let currentScore = 0;
        const interval = setInterval(() => {
            currentScore++;
            scoreDisplay.textContent = `${currentScore}%`;
            
            if (currentScore >= targetScore) {
                clearInterval(interval);
            }
        }, 20);
    }

    updateScoreColor(healthScore) {
        const scoreElement = document.getElementById('healthScore');
        if (!scoreElement) return;
        
        if (healthScore >= 70) {
            scoreElement.style.background = 'linear-gradient(135deg, #06d6a0, #4361ee)';
        } else if (healthScore >= 40) {
            scoreElement.style.background = 'linear-gradient(135deg, #ffd166, #7209b7)';
        } else {
            scoreElement.style.background = 'linear-gradient(135deg, #ef476f, #8338ec)';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.medAnalyzerCharts = new MedAnalyzerCharts();
});