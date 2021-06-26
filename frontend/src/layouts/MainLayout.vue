<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          aria-label="Menu"
          dense
          flat
          icon="menu"
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title class="ecb-font-bold">
          Text Summarizer
        </q-toolbar-title>
        <q-space/>
        <div class="q-gutter-sm row items-center no-wrap ecb-font-regular">
          <q-btn v-if="$q.screen.gt.sm" color="white" icon="menu_book" label="Summarize" push size="sm"
                 text-color="primary" @click="openDialog = true">
            <q-tooltip>Run summarization</q-tooltip>
          </q-btn>
          <q-space/>

        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      content-class="bg-white"
    >
      <q-list>
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Our Application
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataMain"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Used Frameworks
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataFrameworks"
          :key="link.title"
          v-bind="link"
        />
        <q-item-label
          class="text-primary text-bold ecb-font-regular"
          header
        >
          Infrastructure
        </q-item-label>
        <EssentialLink
          v-for="link in linksDataInfrastructure"
          :key="link.title"
          v-bind="link"
        />
      </q-list>

    </q-drawer>

    <q-dialog v-model="openDialog" full-height full-width @close="reset" @hide="reset">
      <div class="row" style="overflow: auto; height: inherit;">
        <div class="col-3" style="background-color: white;">
          <q-card flat square style="overflow: auto;">
            <q-card-section>
              <div class="text-h6 text-primary">Setup</div>
            </q-card-section>
            <q-card-actions align="center">
              <q-btn :disabled="!isComplete" color="primary" label="Summarize" size="sm" unelevated
                     @click="$refs.uploader.upload()">
                <q-tooltip>Run summarization</q-tooltip>
              </q-btn>
              <q-btn color="primary" label="Reset" size="sm" unelevated @click="reset()">
                <q-tooltip>Reset</q-tooltip>
              </q-btn>
              <q-btn color="primary" label="Close" size="sm" unelevated @click="close()">
                <q-tooltip>Close</q-tooltip>
              </q-btn>
            </q-card-actions>
            <q-card-section>
              <q-select
                v-model="topicType"
                :options="optionsTopic"
                dense
                label="Select Topic"
                option-label="label"
                option-value="id"
                outlined
                style="overflow: auto;">
                <template v-slot:prepend>
                  <q-icon name="my_location"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-select
                v-model="summaryType"
                :options="optionsSummary"
                dense
                label="Select Size Of Summary"
                option-label="label"
                option-value="id"
                outlined
                style="overflow: auto;">
                <template v-slot:prepend>
                  <q-icon name="article"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-uploader
                ref="uploader"
                :factory="factoryFn"
                accept=".txt"
                bordered
                color="white"
                flat
                hide-upload-btn
                label="Textfile"
                style="overflow: auto; width: inherit"
                text-color="black"
                @added="setFileSelected"
                @failed="failed"
                @removed="unsetFileSelected"
                @uploaded="summarize"
              />
            </q-card-section>

          </q-card>
        </div>

        <div v-if="summaryVisible" class="col-6" style="background-color: white">
          <q-card flat square style="overflow: auto;">
            <q-card-section>
              <div class="text-h6 text-primary">Summary</div>
            </q-card-section>

            <q-card-actions align="center">
              <q-btn color="primary" label="Download" size="sm" unelevated
                     @click="exportSummary">
                <q-tooltip>Export summary to Textfile</q-tooltip>
              </q-btn>
            </q-card-actions>
            <q-card-section>
              {{ summarization }}
            </q-card-section>
          </q-card>
        </div>

        <div v-if="summaryVisible" class="col-2" style="background-color: white">
          <q-card flat square style="overflow: auto;">
            <q-card-section>
              <div class="text-h6 text-primary">Rating</div>
            </q-card-section>
            <q-card-actions align="center">
              <q-btn color="primary" disabled label="Rate" size="sm" unelevated>
                <q-tooltip>Save rating</q-tooltip>
              </q-btn>
            </q-card-actions>

            <q-card-section>
              <q-rating
                v-model="ratingModel"
                color="primary"
                icon="star_border"
                icon-selected="star"
                size="1.5em"
              />
            </q-card-section>
            <q-card-section>
              By rating the quality of the summary you can improve
              the model quality by providing better training data
              for future model tuning.
              <br><br>
              This feature is not implemented yet.
            </q-card-section>

          </q-card>
        </div>
      </div>
    </q-dialog>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>


</template>

<script>

import EssentialLink from 'components/EssentialLink.vue'
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'

const linksDataMain = [
  {
    title: 'Docs',
    caption: 'See documentation',
    icon: 'school',
    link: 'https://quasar.dev'
  },
  {
    title: 'Our Code',
    caption: 'See code repository',
    icon: 'code',
    link: 'https://github.com/senacor-ecb-tender/summarizer-server'
  }
];

const linksDataFrameworks = [
  {
    title: 'FastAPI',
    caption: 'ASGI python server',
    icon: 'local_library',
    link: 'https://fastapi.tiangolo.com/'
  },
  {
    title: 'Huggingface',
    caption: 'The AI community',
    icon: 'local_library',
    link: 'https://huggingface.co/'
  },
  {
    title: 'Quasar Framework',
    caption: 'Front-End Framework',
    icon: 'local_library',
    link: 'https://quasar.dev/'
  }
];

const linksDataInfrastructure = [
  {
    title: 'Azure Machine Learning',
    caption: 'Integrated Data Science-Solution',
    icon: 'Isettings_input_composite',
    link: 'https://docs.microsoft.com/de-de/azure/machine-learning/overview-what-is-azure-ml'
  },
  {
    title: 'Azure Kubernetes Service',
    caption: 'Easily manage Kubernetes with Azure',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/kubernetes-service//'
  },
  {
    title: 'Azure Static Web Apps',
    caption: 'A serverless web app hosting service',
    icon: 'settings_input_composite',
    link: 'https://azure.microsoft.com/en-us/services/app-service/static'
  },
  {
    title: 'GitHub',
    caption: 'Manage your code',
    icon: 'settings_input_composite',
    link: 'https://github.com/'
  }
];

export default {
  name: 'MainLayout',
  components: {EssentialLink},
  data() {
    return {
      leftDrawerOpen: false,

      linksDataMain: linksDataMain,
      linksDataFrameworks: linksDataFrameworks,
      linksDataInfrastructure: linksDataInfrastructure,

      optionsTopic: [
        {
          id: 'asset_quality',
          label: 'Asset Quality'
        },
        {
          id: 'climate_risk',
          label: 'Climate Risk'
        },
        {
          id: 'pandemic',
          label: 'Pandemic'
        },
        {
          id: 'credit_lending',
          label: 'Credit Lending'
        }
      ],
      optionsSummary: [
        {
          id: 'long',
          label: 'Long version (9-15 sentences)'
        },
        {
          id: 'short',
          label: 'Short version (3-6 sentences)'
        }
      ],
      topicType: "",
      summaryType: "",
      fileSelected: false,
      summarization: "...",
      openDialog: false,
      summaryVisible: false
    }
  },
  setup() {
    const $q = useQuasar()
    return {
      ratingModel: ref(0),
      failed(info) {
        $q.notify({
          type: 'negative',
          message: 'Call to Summarization API failed!'
        })
      }
    }
  },
  computed: {
    isComplete() {
      return this.topicType != "" && this.summaryType != "" && this.fileSelected;
    }
  },
  methods: {
    exportSummary() {
      const $q = useQuasar()

      const status = exportFile('summary.txt', this.summarization, {
        encoding: 'UTF-8',
        mimeType: 'text/plain;charset=UTF-8;'
      })

      if (status === true) {
        // browser allowed it
      } else {
        // browser denied it
        $q.notify({
          type: 'negative',
          message: 'Browser does not allow the export: Error code ' + status
        })
      }
    },
    setFileSelected() {
      this.fileSelected = true
    },
    unsetFileSelected() {
      this.fileSelected = false
    },
    reset() {
      this.summaryVisible = false
      this.summaryType = ""
      this.topicType = ""
      this.fileSelected = false
      this.$refs.uploader.reset()
    },
    close() {
      this.openDialog = false
    },
    factoryFn(files) {
      return {
        url: process.env.API + '/upload',
        method: 'POST',
        fieldName: 'file',
        formFields: [{name: 'topic', value: this.topicType.id}, {name: 'summary_type', value: this.summaryType.id}]
      }
    },
    summarize({files, xhr}) {
      this.summarization = JSON.parse(xhr.response).result
      this.summaryVisible = true
    }
  }
}
</script>
